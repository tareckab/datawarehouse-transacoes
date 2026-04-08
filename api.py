from pathlib import Path
from typing import Any
from datetime import datetime

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from data_processing import fetch_transactions, load_folder_csv, save_transactions
from database import init_db


DATA_FOLDER = Path(__file__).resolve().parent / "dados"
ALLOWED_FIELDS = {"kpis", "daily", "monthly", "yearly", "categories", "month_comparison", "transactions"}

app = FastAPI(title="Dashboard API", version="1.0.0")
LAST_SYNC_AT: datetime | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def sync_from_data_folder() -> int:
    global LAST_SYNC_AT
    if not DATA_FOLDER.exists():
        LAST_SYNC_AT = datetime.now()
        return 0
    df_folder = load_folder_csv(DATA_FOLDER)
    inserted = save_transactions(df_folder)
    LAST_SYNC_AT = datetime.now()
    return inserted


def _apply_filters(df, months: list[str], categories: list[str]):
    out = df.copy()

    if months and "Todos" not in months:
        out = out[out["mes_ano"].isin(months)]

    if categories and "Todos" not in categories:
        out = out[out["categoria"].isin(categories)]

    return out


def _to_float(value: Any) -> float:
    return float(value) if value is not None else 0.0


def _normalize_fields(fields: list[str]) -> set[str]:
    if not fields:
        return {"kpis", "monthly", "yearly", "categories", "month_comparison"}

    normalized = {field.strip().lower() for field in fields if field and field.strip()}
    selected = normalized.intersection(ALLOWED_FIELDS)
    return selected or {"kpis", "monthly", "yearly", "categories", "month_comparison"}


def _empty_dashboard_payload(selected_fields: set[str]) -> dict[str, Any]:
    payload: dict[str, Any] = {"updated_at": LAST_SYNC_AT.isoformat() if LAST_SYNC_AT else None}

    if "kpis" in selected_fields:
        payload["kpis"] = {"total": 0, "count": 0, "avg": 0, "max": 0}
    if "daily" in selected_fields:
        payload["daily"] = []
    if "monthly" in selected_fields:
        payload["monthly"] = []
    if "yearly" in selected_fields:
        payload["yearly"] = []
    if "categories" in selected_fields:
        payload["categories"] = []
    if "month_comparison" in selected_fields:
        payload["month_comparison"] = None
    if "transactions" in selected_fields:
        payload["transactions"] = []

    return payload


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    sync_from_data_folder()


@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": True}


@app.post("/api/sync")
def sync() -> dict[str, Any]:
    inserted = sync_from_data_folder()
    return {"inserted": inserted}


@app.get("/api/filters")
def filters() -> dict[str, Any]:
    df = fetch_transactions()
    if df.empty:
        return {"months": [], "categories": []}

    months = sorted(df["mes_ano"].unique().tolist())
    categories = sorted(df["categoria"].unique().tolist())
    return {"months": months, "categories": categories}


@app.get("/api/dashboard")
def dashboard(
    months: list[str] = Query(default=[]),
    categories: list[str] = Query(default=[]),
    fields: list[str] = Query(default=[]),
) -> dict[str, Any]:
    selected_fields = _normalize_fields(fields)
    df = fetch_transactions()
    if df.empty:
        return _empty_dashboard_payload(selected_fields)

    filtered = _apply_filters(df, months, categories)

    if filtered.empty:
        return _empty_dashboard_payload(selected_fields)

    filtered_spend = filtered[filtered["valor"] > 0].copy()

    payload: dict[str, Any] = {"updated_at": LAST_SYNC_AT.isoformat() if LAST_SYNC_AT else None}

    if "kpis" in selected_fields:
        if filtered_spend.empty:
            payload["kpis"] = {"total": 0, "count": 0, "avg": 0, "max": 0}
        else:
            payload["kpis"] = {
                "total": _to_float(filtered_spend["valor"].sum()),
                "count": int(len(filtered_spend)),
                "avg": _to_float(filtered_spend["valor"].mean()),
                "max": _to_float(filtered_spend["valor"].max()),
            }

    if "daily" in selected_fields:
        by_day = filtered_spend.groupby(filtered_spend["data_compra"].dt.strftime("%Y-%m-%d"), as_index=False)["valor"].sum()
        payload["daily"] = [{"data": row["data_compra"], "valor": _to_float(row["valor"])} for _, row in by_day.iterrows()]

    if "categories" in selected_fields:
        by_category = filtered_spend.groupby("categoria", as_index=False)["valor"].sum().sort_values("valor", ascending=False)
        payload["categories"] = [{"categoria": row["categoria"], "valor": _to_float(row["valor"])} for _, row in by_category.iterrows()]

    if "monthly" in selected_fields:
        by_month = filtered_spend.groupby("mes_ano", as_index=False)["valor"].sum().sort_values("mes_ano")
        payload["monthly"] = [{"mes_ano": row["mes_ano"], "valor": _to_float(row["valor"])} for _, row in by_month.iterrows()]

    if "yearly" in selected_fields:
        filtered_with_year = filtered_spend.copy()
        filtered_with_year["ano"] = filtered_with_year["data_compra"].dt.year.astype(str)
        by_year = filtered_with_year.groupby("ano", as_index=False)["valor"].sum().sort_values("ano")
        payload["yearly"] = [{"ano": row["ano"], "valor": _to_float(row["valor"])} for _, row in by_year.iterrows()]

    if "month_comparison" in selected_fields:
        month_totals = df.groupby("mes_ano", as_index=False)["valor"].sum().sort_values("mes_ano")
        month_comparison = None
        if len(month_totals) >= 2:
            current = month_totals.iloc[-1]
            previous = month_totals.iloc[-2]
            delta = _to_float(current["valor"] - previous["valor"])
            month_comparison = {
                "current_month": current["mes_ano"],
                "previous_month": previous["mes_ano"],
                "delta": delta,
                "direction": "aumento" if delta > 0 else "reducao",
            }
        payload["month_comparison"] = month_comparison

    if "transactions" in selected_fields:
        tx = filtered.sort_values("data_compra", ascending=False).head(100)
        payload["transactions"] = [
            {
                "data_compra": row["data_compra"].strftime("%Y-%m-%d"),
                "descricao": row["descricao"],
                "categoria": row["categoria"],
                "valor": _to_float(row["valor"]),
            }
            for _, row in tx.iterrows()
        ]

    return payload

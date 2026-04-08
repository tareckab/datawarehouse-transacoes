from pathlib import Path
from typing import Iterable

import pandas as pd
from sqlalchemy.dialects.sqlite import insert

from database import SessionLocal
from models import Transaction
from utils import build_transaction_hash, infer_category


COLUMN_ALIASES = {
    "Data de Compra": "data_compra",
    "data_compra": "data_compra",
    "Descrição": "descricao",
    "descricao": "descricao",
    "Valor (em R$)": "valor",
    "valor": "valor",
    "Categoria": "categoria",
    "categoria": "categoria",
}


def _rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns={col: COLUMN_ALIASES.get(col, col) for col in df.columns})


def _sanitize_frame(df: pd.DataFrame, source_file: str) -> pd.DataFrame:
    df = _rename_columns(df).copy()

    required = ["data_compra", "descricao", "valor"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Arquivo {source_file} sem colunas obrigatorias: {missing}")

    if "categoria" not in df.columns:
        df["categoria"] = None

    df["data_compra"] = pd.to_datetime(df["data_compra"], errors="coerce", dayfirst=True)
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["descricao"] = df["descricao"].astype(str).str.strip()
    df["categoria"] = df["categoria"].astype(str).str.strip()

    df = df.dropna(subset=["data_compra", "valor", "descricao"]).copy()
    df = df[df["descricao"] != ""]

    df.loc[df["categoria"].isin(["", "-", "nan", "none", "None"]), "categoria"] = None
    df["categoria"] = df.apply(
        lambda row: row["categoria"] if pd.notna(row["categoria"]) else infer_category(row["descricao"]),
        axis=1,
    )

    df["mes_ano"] = df["data_compra"].dt.to_period("M").astype(str)
    df["source_file"] = source_file
    df["tx_hash"] = df.apply(
        lambda row: build_transaction_hash(
            row["data_compra"].strftime("%Y-%m-%d"),
            row["descricao"],
            row["valor"],
            row["categoria"],
            source_file,
        ),
        axis=1,
    )

    return df[["data_compra", "mes_ano", "descricao", "categoria", "valor", "source_file", "tx_hash"]]


def load_uploaded_files(files: Iterable) -> pd.DataFrame:
    frames = []
    for uploaded_file in files:
        df = pd.read_csv(uploaded_file, sep=None, engine="python")
        frames.append(_sanitize_frame(df, uploaded_file.name))

    if not frames:
        return pd.DataFrame(columns=["data_compra", "mes_ano", "descricao", "categoria", "valor", "source_file", "tx_hash"])

    return pd.concat(frames, ignore_index=True)


def load_folder_csv(folder: Path) -> pd.DataFrame:
    frames = []
    for csv_file in sorted(folder.glob("*.csv")):
        df = pd.read_csv(csv_file, sep=";", encoding="utf-8")
        frames.append(_sanitize_frame(df, csv_file.name))

    if not frames:
        return pd.DataFrame(columns=["data_compra", "mes_ano", "descricao", "categoria", "valor", "source_file", "tx_hash"])

    return pd.concat(frames, ignore_index=True)


def save_transactions(df: pd.DataFrame) -> int:
    if df.empty:
        return 0

    records = df.to_dict(orient="records")
    inserted = 0

    with SessionLocal() as session:
        for record in records:
            stmt = insert(Transaction).values(**record)
            stmt = stmt.on_conflict_do_nothing(index_elements=["tx_hash"])
            result = session.execute(stmt)
            inserted += result.rowcount or 0
        session.commit()

    return inserted


def fetch_transactions() -> pd.DataFrame:
    with SessionLocal() as session:
        rows = session.query(Transaction).all()

    if not rows:
        return pd.DataFrame(columns=["id", "data_compra", "mes_ano", "descricao", "categoria", "valor", "source_file"])

    data = [
        {
            "id": row.id,
            "data_compra": row.data_compra,
            "mes_ano": row.mes_ano,
            "descricao": row.descricao,
            "categoria": row.categoria,
            "valor": row.valor,
            "source_file": row.source_file,
        }
        for row in rows
    ]
    df = pd.DataFrame(data)
    df["data_compra"] = pd.to_datetime(df["data_compra"])
    return df

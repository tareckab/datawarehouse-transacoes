from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dw.db"

st.set_page_config(page_title="Dashboard ETL - Cartoes", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Manrope', sans-serif;
        }

        .stApp {
            background: radial-gradient(circle at 15% 15%, #f5f1e6 0%, #f6f8fb 45%, #e9edf4 100%);
        }

        .hero {
            padding: 1.2rem 1.4rem;
            border-radius: 16px;
            background: linear-gradient(110deg, #0c3b2e, #2f5d50);
            color: #f2f6f4;
            box-shadow: 0 10px 24px rgba(10, 41, 32, 0.25);
            margin-bottom: 1.1rem;
        }

        .kpi {
            padding: 0.8rem 1rem;
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.75);
            border: 1px solid rgba(12, 59, 46, 0.12);
            box-shadow: 0 6px 16px rgba(10, 41, 32, 0.08);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def _load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame()

    engine = create_engine(f"sqlite:///{DB_PATH}")
    query = """
        SELECT
            f.id,
            d.data,
            d.dia,
            d.mes,
            d.ano,
            d.trimestre,
            d.dia_semana,
            t.nome_titular,
            t.final_cartao,
            c.nome_categoria,
            e.nome_estabelecimento,
            f.valor_brl,
            f.valor_usd,
            f.cotacao,
            f.parcela_texto,
            f.num_parcela,
            f.total_parcelas,
            f.arquivo_origem
        FROM fato_transacao f
        JOIN dim_data d ON d.id_data = f.id_data
        JOIN dim_titular t ON t.id_titular = f.id_titular
        JOIN dim_categoria c ON c.id_categoria = f.id_categoria
        JOIN dim_estabelecimento e ON e.id_estabelecimento = f.id_estabelecimento
    """
    df = pd.read_sql(query, engine)
    df["data"] = pd.to_datetime(df["data"])
    return df


df = _load_data()

st.markdown(
    """
    <div class='hero'>
        <h2 style='margin:0;'>Dashboard de Transacoes (ETL)</h2>
        <p style='margin:0.25rem 0 0 0;'>Visao consolidada dos dados extraidos, tratados e carregados no Data Warehouse.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if df.empty:
    st.warning("Banco nao encontrado ou sem dados. Execute: python etl/main.py")
    st.stop()

col_f1, col_f2, col_f3, col_f4 = st.columns([1.4, 1.2, 1.2, 1.2])

with col_f1:
    data_ini = st.date_input("Data inicial", value=df["data"].min().date())
with col_f2:
    data_fim = st.date_input("Data final", value=df["data"].max().date())
with col_f3:
    titulares = st.multiselect("Titulares", sorted(df["nome_titular"].unique().tolist()))
with col_f4:
    categorias = st.multiselect("Categorias", sorted(df["nome_categoria"].unique().tolist()))

filtrado = df[(df["data"].dt.date >= data_ini) & (df["data"].dt.date <= data_fim)].copy()
if titulares:
    filtrado = filtrado[filtrado["nome_titular"].isin(titulares)]
if categorias:
    filtrado = filtrado[filtrado["nome_categoria"].isin(categorias)]

if filtrado.empty:
    st.info("Nenhum registro encontrado para os filtros selecionados.")
    st.stop()

total_gasto = filtrado["valor_brl"].sum()
media_ticket = filtrado["valor_brl"].mean()
qtd = len(filtrado)
qtd_cat = filtrado["nome_categoria"].nunique()

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"<div class='kpi'><b>Gasto total</b><br>R$ {total_gasto:,.2f}</div>", unsafe_allow_html=True)
k2.markdown(f"<div class='kpi'><b>Ticket medio</b><br>R$ {media_ticket:,.2f}</div>", unsafe_allow_html=True)
k3.markdown(f"<div class='kpi'><b>Transacoes</b><br>{qtd}</div>", unsafe_allow_html=True)
k4.markdown(f"<div class='kpi'><b>Categorias ativas</b><br>{qtd_cat}</div>", unsafe_allow_html=True)

serie_mensal = (
    filtrado.assign(ano_mes=filtrado["data"].dt.to_period("M").astype(str))
    .groupby("ano_mes", as_index=False)["valor_brl"]
    .sum()
)
fig_mensal = px.line(
    serie_mensal,
    x="ano_mes",
    y="valor_brl",
    markers=True,
    title="Evolucao mensal do gasto (R$)",
    color_discrete_sequence=["#0c3b2e"],
)
fig_mensal.update_layout(plot_bgcolor="rgba(255,255,255,0.65)", paper_bgcolor="rgba(0,0,0,0)")

cat_top = (
    filtrado.groupby("nome_categoria", as_index=False)["valor_brl"]
    .sum()
    .sort_values("valor_brl", ascending=False)
    .head(10)
)
fig_cat = px.bar(
    cat_top,
    x="valor_brl",
    y="nome_categoria",
    orientation="h",
    title="Top 10 categorias por gasto",
    color="valor_brl",
    color_continuous_scale="Teal",
)
fig_cat.update_layout(plot_bgcolor="rgba(255,255,255,0.65)", paper_bgcolor="rgba(0,0,0,0)")

col_g1, col_g2 = st.columns(2)
col_g1.plotly_chart(fig_mensal, use_container_width=True)
col_g2.plotly_chart(fig_cat, use_container_width=True)

titular_gasto = (
    filtrado.groupby(["nome_titular", "final_cartao"], as_index=False)["valor_brl"]
    .sum()
    .sort_values("valor_brl", ascending=False)
)
fig_titular = px.pie(
    titular_gasto,
    names="nome_titular",
    values="valor_brl",
    title="Distribuicao de gasto por titular",
    hole=0.45,
)
fig_titular.update_layout(paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_titular, use_container_width=True)

st.subheader("Detalhamento das transacoes")
colunas = [
    "data",
    "nome_titular",
    "final_cartao",
    "nome_categoria",
    "nome_estabelecimento",
    "valor_brl",
    "valor_usd",
    "parcela_texto",
    "arquivo_origem",
]
st.dataframe(filtrado[colunas].sort_values("data", ascending=False), use_container_width=True)

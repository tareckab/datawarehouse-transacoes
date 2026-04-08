
import sqlite3
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "dw.db"
SQL_PATH = BASE_DIR / "sql" / "create_tables.sql"
engine = create_engine(f"sqlite:///{DB_PATH}")


def create_tables() -> None:
    with open(SQL_PATH, encoding="utf-8") as f:
        sql = f.read()

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.executescript(sql)


def _clear_tables(conn) -> None:
    conn.execute(text("DELETE FROM fato_transacao"))
    conn.execute(text("DELETE FROM dim_data"))
    conn.execute(text("DELETE FROM dim_titular"))
    conn.execute(text("DELETE FROM dim_categoria"))
    conn.execute(text("DELETE FROM dim_estabelecimento"))


def load(df: pd.DataFrame) -> None:
    with engine.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys = ON"))
        _clear_tables(conn)

        dim_data = df[['data', 'dia', 'mes', 'ano', 'trimestre', 'dia_semana']].drop_duplicates().copy()
        dim_data.to_sql('dim_data', conn, if_exists='append', index=False)

        dim_titular = df[['Nome no Cartão', 'Final do Cartão']].drop_duplicates().copy()
        dim_titular.columns = ['nome_titular', 'final_cartao']
        dim_titular.to_sql('dim_titular', conn, if_exists='append', index=False)

        dim_categoria = df[['Categoria']].drop_duplicates().copy()
        dim_categoria.columns = ['nome_categoria']
        dim_categoria.to_sql('dim_categoria', conn, if_exists='append', index=False)

        dim_est = df[['Descricao_limpa']].drop_duplicates().copy()
        dim_est.columns = ['nome_estabelecimento']
        dim_est.to_sql('dim_estabelecimento', conn, if_exists='append', index=False)

        map_data = pd.read_sql(
            "SELECT id_data, data, dia, mes, ano, trimestre, dia_semana FROM dim_data",
            conn,
        )
        map_data['data'] = pd.to_datetime(map_data['data'])
        map_titular = pd.read_sql(
            "SELECT id_titular, nome_titular, final_cartao FROM dim_titular",
            conn,
        )
        map_categoria = pd.read_sql(
            "SELECT id_categoria, nome_categoria FROM dim_categoria",
            conn,
        )
        map_est = pd.read_sql(
            "SELECT id_estabelecimento, nome_estabelecimento FROM dim_estabelecimento",
            conn,
        )

        fato = df.copy()
        fato = fato.merge(
            map_data,
            on=['data', 'dia', 'mes', 'ano', 'trimestre', 'dia_semana'],
            how='left',
        )
        fato = fato.merge(
            map_titular,
            left_on=['Nome no Cartão', 'Final do Cartão'],
            right_on=['nome_titular', 'final_cartao'],
            how='left',
        )
        fato = fato.merge(
            map_categoria,
            left_on='Categoria',
            right_on='nome_categoria',
            how='left',
        )
        fato = fato.merge(
            map_est,
            left_on='Descricao_limpa',
            right_on='nome_estabelecimento',
            how='left',
        )

        fato_out = fato[
            [
                'id_data',
                'id_titular',
                'id_categoria',
                'id_estabelecimento',
                'valor_brl',
                'valor_usd',
                'cotacao',
                'Parcela',
                'num_parcela',
                'total_parcelas',
                'arquivo_origem',
            ]
        ].copy()
        fato_out.columns = [
            'id_data',
            'id_titular',
            'id_categoria',
            'id_estabelecimento',
            'valor_brl',
            'valor_usd',
            'cotacao',
            'parcela_texto',
            'num_parcela',
            'total_parcelas',
            'arquivo_origem',
        ]

        fato_out.to_sql('fato_transacao', conn, if_exists='append', index=False)

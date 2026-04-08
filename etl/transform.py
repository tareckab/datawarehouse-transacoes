
import pandas as pd

def tratar_parcela(p):
    try:
        if pd.isna(p) or p == '-' or p == 'Única':
            return 1, 1
        x, y = p.split('/')
        return int(x), int(y)
    except:
        return 1, 1

def transform(df):
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    text_columns = ['Nome no Cartão', 'Final do Cartão', 'Categoria', 'Descrição', 'Parcela']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df['data'] = pd.to_datetime(df['Data de Compra'], format='%d/%m/%Y', errors='coerce')
    df = df[df['data'].notna()].copy()

    df['dia'] = df['data'].dt.day
    df['mes'] = df['data'].dt.month
    df['ano'] = df['data'].dt.year
    df['trimestre'] = df['data'].dt.quarter
    df['dia_semana'] = df['data'].dt.day_name()

    df['valor_brl'] = pd.to_numeric(df['Valor (em R$)'], errors='coerce').fillna(0)
    df['valor_usd'] = pd.to_numeric(df.get('Valor (em US$)', 0), errors='coerce').fillna(0)
    df['cotacao'] = pd.to_numeric(df.get('Cotação (em R$)', 0), errors='coerce').fillna(0)

    df['Categoria'] = df['Categoria'].replace({'-': 'Nao categorizado', 'nan': 'Nao categorizado'}).fillna('Nao categorizado')
    df['Descricao_limpa'] = df['Descrição'].replace({'nan': 'Sem descricao'}).fillna('Sem descricao')

    parcelas = df['Parcela'].apply(tratar_parcela)
    df['num_parcela'] = parcelas.apply(lambda x: x[0])
    df['total_parcelas'] = parcelas.apply(lambda x: x[1])

    return df

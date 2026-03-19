
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
    df['data'] = pd.to_datetime(df['Data de Compra'], format='%d/%m/%Y', errors='coerce')

    df['dia'] = df['data'].dt.day
    df['mes'] = df['data'].dt.month
    df['ano'] = df['data'].dt.year
    df['trimestre'] = df['data'].dt.quarter
    df['dia_semana'] = df['data'].dt.day_name()

    df['valor_brl'] = pd.to_numeric(df['Valor (em R$)'], errors='coerce')
    df['valor_usd'] = pd.to_numeric(df.get('Valor (em US$)', 0), errors='coerce')
    df['cotacao'] = pd.to_numeric(df.get('Cotação', 0), errors='coerce')

    df['Categoria'] = df['Categoria'].replace('-', 'Não categorizado')

    parcelas = df['Parcela'].apply(tratar_parcela)
    df['num_parcela'] = parcelas.apply(lambda x: x[0])
    df['total_parcelas'] = parcelas.apply(lambda x: x[1])

    return df

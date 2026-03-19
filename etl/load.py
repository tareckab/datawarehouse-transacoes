
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///../dw.db")

def create_tables():
    with open("../sql/create_tables.sql") as f:
        sql = f.read()
    with engine.connect() as conn:
        conn.execute(text(sql))

def load(df):
    dim_data = df[['data','dia','mes','ano','trimestre','dia_semana']].drop_duplicates()
    dim_data.to_sql('dim_data', engine, if_exists='append', index=False)

    dim_titular = df[['Nome no Cartão','Final do Cartão']].drop_duplicates()
    dim_titular.columns = ['nome_titular','final_cartao']
    dim_titular.to_sql('dim_titular', engine, if_exists='append', index=False)

    dim_categoria = df[['Categoria']].drop_duplicates()
    dim_categoria.columns = ['nome_categoria']
    dim_categoria.to_sql('dim_categoria', engine, if_exists='append', index=False)

    dim_est = df[['Descrição']].drop_duplicates()
    dim_est.columns = ['nome_estabelecimento']
    dim_est.to_sql('dim_estabelecimento', engine, if_exists='append', index=False)

    fato = df[['valor_brl','valor_usd','cotacao','Parcela','num_parcela','total_parcelas']]
    fato.columns = ['valor_brl','valor_usd','cotacao','parcela_texto','num_parcela','total_parcelas']
    fato.to_sql('fato_transacao', engine, if_exists='append', index=False)

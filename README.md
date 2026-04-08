
# Projeto Data Warehouse - Transacoes de Cartao

## Objetivo
Construir um Data Warehouse a partir de dados de faturas de cartao de credito, aplicando ETL completo (extracao, transformacao/limpeza e carga) e consumo analitico em dashboard interativo.

## Tecnologias
- Python (pandas)
- SQLite
- SQLAlchemy
- Streamlit
- Plotly

## Estrutura
- etl/: scripts ETL
- sql/: criacao de tabelas e queries
- dados/: arquivos CSV
- dashboard/: aplicacao interativa para analise

## Execução
1. Instale dependências:
   pip install -r requirements.txt

2. Coloque os CSVs na pasta dados/

3. Execute o ETL:
   python etl/main.py

4. Execute o dashboard:
   python -m streamlit run dashboard/app.py

## Consultas
Veja sql/queries.sql

## Resultado esperado
- Banco `dw.db` preenchido com modelo dimensional (dimensoes e fato).
- Consultas SQL funcionando com joins corretos.
- Dashboard interativo com filtros, KPIs, graficos e tabela de detalhamento.

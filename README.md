
# Projeto Data Warehouse - Transacoes de Cartao

## Objetivo
Construir um Data Warehouse a partir de dados de faturas de cartao de credito, aplicando ETL completo (extracao, transformacao/limpeza e carga) e consumo analitico em dashboard interativo.

## Tecnologias
- Python (pandas)
- SQLite
- SQLAlchemy
- FastAPI
- Vue 3 (Vite)
- Plotly.js

## Estrutura
- api.py: backend Python para disponibilizar os dados
- database.py: configuracao SQLite + SQLAlchemy
- models.py: modelos ORM
- data_processing.py: tratamento e persistencia dos CSVs
- utils.py: funcoes auxiliares
- dados/: arquivos CSV
- frontend/: aplicacao Vue do dashboard

## Execução
1. Instale dependências:
   pip install -r requirements.txt

2. Coloque os CSVs na pasta dados/

3. Inicie o backend Python:
   python -m uvicorn api:app --host 127.0.0.1 --port 8000

4. Em outro terminal, inicie o frontend:
   cd frontend
   npm install
   npm run dev

5. Opcional: execute o ETL dimensional legado:
   python etl/main.py

## Consultas
Veja sql/queries.sql

## Resultado esperado
- Banco `dw.db` preenchido com modelo dimensional (dimensoes e fato).
- Consultas SQL funcionando com joins corretos.
- Dashboard interativo com filtros, KPIs, graficos e tabela de detalhamento.

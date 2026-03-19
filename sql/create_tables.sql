
CREATE TABLE IF NOT EXISTS dim_data (
    id_data INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    dia INTEGER,
    mes INTEGER,
    trimestre INTEGER,
    ano INTEGER,
    dia_semana TEXT
);

CREATE TABLE IF NOT EXISTS dim_titular (
    id_titular INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_titular TEXT,
    final_cartao TEXT
);

CREATE TABLE IF NOT EXISTS dim_categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT
);

CREATE TABLE IF NOT EXISTS dim_estabelecimento (
    id_estabelecimento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_estabelecimento TEXT
);

CREATE TABLE IF NOT EXISTS fato_transacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_data INTEGER,
    id_titular INTEGER,
    id_categoria INTEGER,
    id_estabelecimento INTEGER,
    valor_brl REAL,
    valor_usd REAL,
    cotacao REAL,
    parcela_texto TEXT,
    num_parcela INTEGER,
    total_parcelas INTEGER
);

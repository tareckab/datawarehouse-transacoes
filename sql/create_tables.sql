
CREATE TABLE IF NOT EXISTS dim_data (
    id_data INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE,
    dia INTEGER,
    mes INTEGER,
    trimestre INTEGER,
    ano INTEGER,
    dia_semana TEXT,
    UNIQUE(data, dia, mes, trimestre, ano, dia_semana)
);

CREATE TABLE IF NOT EXISTS dim_titular (
    id_titular INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_titular TEXT,
    final_cartao TEXT,
    UNIQUE(nome_titular, final_cartao)
);

CREATE TABLE IF NOT EXISTS dim_categoria (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_categoria TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_estabelecimento (
    id_estabelecimento INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_estabelecimento TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS fato_transacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_data INTEGER NOT NULL,
    id_titular INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    id_estabelecimento INTEGER NOT NULL,
    valor_brl REAL,
    valor_usd REAL,
    cotacao REAL,
    parcela_texto TEXT,
    num_parcela INTEGER,
    total_parcelas INTEGER,
    arquivo_origem TEXT,
    FOREIGN KEY (id_data) REFERENCES dim_data(id_data),
    FOREIGN KEY (id_titular) REFERENCES dim_titular(id_titular),
    FOREIGN KEY (id_categoria) REFERENCES dim_categoria(id_categoria),
    FOREIGN KEY (id_estabelecimento) REFERENCES dim_estabelecimento(id_estabelecimento)
);

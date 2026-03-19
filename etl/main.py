
from extract import extract
from transform import transform
from load import load, create_tables

def main():
    create_tables()
    df = extract()
    df = transform(df)
    load(df)
    print("ETL finalizado com sucesso!")

if __name__ == "__main__":
    main()

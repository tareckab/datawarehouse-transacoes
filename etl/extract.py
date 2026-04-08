
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_CANDIDATES = [BASE_DIR / "dados", BASE_DIR / "data"]


def _get_data_dir() -> Path:
    for candidate in DATA_CANDIDATES:
        if candidate.exists() and candidate.is_dir():
            return candidate
    raise FileNotFoundError("Nenhuma pasta de dados encontrada (esperado: 'dados/' ou 'data/').")


def extract() -> pd.DataFrame:
    data_dir = _get_data_dir()
    csv_files = sorted(data_dir.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {data_dir}")

    frames = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file, sep=";", encoding="utf-8")
        df["arquivo_origem"] = csv_file.name
        frames.append(df)

    return pd.concat(frames, ignore_index=True)

import hashlib
import re


def slug_text(value: str) -> str:
    value = (value or "").strip().lower()
    return re.sub(r"\s+", " ", value)


def infer_category(description: str) -> str:
    text = slug_text(description)

    rules = {
        "mercado": ["mercado", "super", "zaffari", "walmart", "portella", "cotrijal"],
        "uber": ["uber", "99", "taxi"],
        "restaurante": ["restaurante", "lanch", "bar", "ifood", "pizza", "pub"],
        "assinaturas": ["openai", "spotify", "netflix", "amazon music", "microsoft"],
        "combustivel": ["posto", "gas", "ipiranga", "shell"],
    }

    for category, keywords in rules.items():
        if any(keyword in text for keyword in keywords):
            return category

    return "outros"


def build_transaction_hash(data_compra: str, descricao: str, valor: float, categoria: str, source_file: str) -> str:
    raw = f"{data_compra}|{slug_text(descricao)}|{float(valor):.2f}|{slug_text(categoria)}|{source_file}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

from constants.abbreviations import abbreviations
import re


def format_name(name: str) -> str:
    name = name.strip()

    name = re.sub(r" & ", " e ", name)

    # remove pontuação (mantém acentos) e números
    name = re.sub(r"[^\w\s]", " ", name, flags=re.UNICODE)
    name = re.sub(r"\d+", " ", name)  # Remove dígitos

    name = name.title()

    # Aplica abreviações (case-insensitive)
    for key, value in abbreviations.items():
        pattern = re.compile(rf"\b{re.escape(key)}\b", flags=re.IGNORECASE)
        name = pattern.sub(value, name)

    name = re.sub(r"\s+", " ", name).strip()  # Colapsa espaços repetidos
    return name

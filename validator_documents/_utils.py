"""Utilitários compartilhados pelos validadores."""

from __future__ import annotations

import re


def normalizar(dado: str | int) -> str:
    """Remove todos os caracteres que não são dígitos.

    Aceita ``str`` (com ou sem máscara) ou ``int``. Retorna a sequência de
    dígitos como ``str``.
    """
    if isinstance(dado, str):
        return re.sub(r"\D", "", dado)
    if isinstance(dado, int):
        return str(dado)
    raise ValueError("O dado deve ser uma string ou um número inteiro.")


def tem_digitos_repetidos(digitos: str) -> bool:
    """Indica se todos os dígitos são iguais (ex.: ``11111111111``)."""
    return len(set(digitos)) == 1

"""Validação e formatação de placas veiculares brasileiras.

Suporta dois padrões:
- Antigo: ``ABC-1234`` (3 letras + 4 dígitos)
- Mercosul: ``ABC1D23`` (3 letras + 1 dígito + 1 letra + 2 dígitos)

Não há dígito verificador — validação é apenas por formato/regex.
"""

from __future__ import annotations

import re

_PLACA_ANTIGA = re.compile(r"^[A-Z]{3}\d{4}$")
_PLACA_MERCOSUL = re.compile(r"^[A-Z]{3}\d[A-Z]\d{2}$")


def _normalizar_placa(placa: str | int) -> str:
    s = str(placa).upper().strip()
    return re.sub(r"[^A-Z0-9]", "", s)


def _eh_placa_valida(normalizada: str) -> bool:
    return bool(_PLACA_ANTIGA.fullmatch(normalizada) or _PLACA_MERCOSUL.fullmatch(normalizada))


def validar_placa(placa: str | int) -> bool:
    """Valida uma placa pelo formato (antigo ou Mercosul)."""
    return _eh_placa_valida(_normalizar_placa(placa))


def formatar_placa(placa: str | int) -> str:
    """Formata a placa:
    - Antigo: ``ABC-1234``
    - Mercosul: ``ABC1D23`` (sem hífen, padrão oficial)
    """
    n = _normalizar_placa(placa)
    if _PLACA_ANTIGA.fullmatch(n):
        return f"{n[:3]}-{n[3:]}"
    if _PLACA_MERCOSUL.fullmatch(n):
        return n  # padrão Mercosul oficial sem hífen
    raise ValueError("Formato de placa inválido para formatação.")


def gerar_placa(mercosul: bool = False) -> str:
    """Gera uma placa válida aleatória.

    Args:
        mercosul: Se True, gera padrão Mercosul; se False, padrão antigo.

    Returns:
        Placa formatada (antigo com hífen, Mercosul sem hífen).
    """
    import random

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    digitos = "0123456789"

    if mercosul:
        # ABC1D23
        n = (
            "".join(random.choices(letras, k=3))
            + random.choice(digitos)
            + random.choice(letras)
            + "".join(random.choices(digitos, k=2))
        )
        return n  # sem hífen
    else:
        # ABC-1234
        n = "".join(random.choices(letras, k=3)) + "".join(random.choices(digitos, k=4))
        return f"{n[:3]}-{n[3:]}"

"""Validação e formatação de RENAVAM (Registro Nacional de Veículos Automotores).

Algoritmo: módulo 11 com pesos fixos sobre os 10 primeiros dígitos.
"""

from __future__ import annotations

from ._utils import normalizar

_TAMANHO = 11

_PESOS = (3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def validar_renavam(renavam: str | int) -> bool:
    """Valida um RENAVAM pelo dígito verificador."""
    renavam = normalizar(renavam)
    if len(renavam) != _TAMANHO:
        return False

    total = sum(int(d) * p for d, p in zip(renavam[:10], _PESOS, strict=False))
    resto = (total * 10) % 11
    digito = 0 if resto == 10 else resto
    return renavam[-1] == str(digito)


def formatar_renavam(renavam: str | int) -> str:
    """Formata um RENAVAM no padrão ``XXXXXXXXXX-X``."""
    renavam = normalizar(renavam)
    if len(renavam) != _TAMANHO:
        raise ValueError("RENAVAM deve conter 11 dígitos para formatação.")
    return f"{renavam[:10]}-{renavam[10:]}"


def gerar_renavam() -> str:
    """Gera um RENAVAM válido aleatório formatado."""
    import random

    base = [str(random.randint(0, 9)) for _ in range(10)]
    total = sum(int(d) * p for d, p in zip(base, _PESOS, strict=False))
    resto = (total * 10) % 11
    digito = 0 if resto == 10 else resto
    base.append(str(digito))
    renavam = "".join(base)
    return formatar_renavam(renavam)

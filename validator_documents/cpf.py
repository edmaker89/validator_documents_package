"""Validação e formatação de CPF.

Fonte do algoritmo: módulo 11, dígitos verificadores calculados com pesos
decrescentes de 10 a 2 (primeiro DV) e de 11 a 2 (segundo DV).
"""

from __future__ import annotations

from ._utils import normalizar, tem_digitos_repetidos

_TAMANHO = 11


def _digito_verificador(digitos: str, pesos: tuple[int, ...]) -> int:
    resto = sum(int(d) * p for d, p in zip(digitos, pesos, strict=False)) % 11
    return 0 if resto < 2 else 11 - resto


def validar_cpf(cpf: str | int) -> bool:
    """Valida um CPF pelos dígitos verificadores."""
    cpf = normalizar(cpf)
    if len(cpf) != _TAMANHO or tem_digitos_repetidos(cpf):
        return False

    primeiro = _digito_verificador(cpf[:9], tuple(range(10, 1, -1)))
    segundo = _digito_verificador(cpf[:10], tuple(range(11, 1, -1)))
    return cpf[-2:] == f"{primeiro}{segundo}"


def formatar_cpf(cpf: str | int) -> str:
    """Formata um CPF no padrão ``XXX.XXX.XXX-XX``."""
    cpf = normalizar(cpf)
    if len(cpf) != _TAMANHO:
        raise ValueError("CPF deve conter 11 dígitos para formatação.")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def gerar_cpf() -> str:
    """Gera um CPF válido aleatório formatado."""
    import random

    base = [str(random.randint(0, 9)) for _ in range(9)]
    primeiro = _digito_verificador("".join(base), tuple(range(10, 1, -1)))
    base.append(str(primeiro))
    segundo = _digito_verificador("".join(base), tuple(range(11, 1, -1)))
    base.append(str(segundo))
    cpf = "".join(base)
    return formatar_cpf(cpf)

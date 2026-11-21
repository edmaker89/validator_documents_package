"""Validação e formatação de CNH (Carteira Nacional de Habilitação).

Algoritmo oficial (baseado em validate-docbr e legislação):
- 11 dígitos; 9 primeiros são o registro, 2 últimos são DVs.
- Primeiro DV: pesos 9..1 sobre os 9 primeiros dígitos, módulo 11.
  Se resto >= 10 → DV = 0 e _dsc = 2; caso contrário _dsc = 0.
- Segundo DV: pesos 1..9 sobre os 9 primeiros dígitos, módulo 11.
  DV = resto - _dsc; se < 0 → +11; se >= 10 → 0.
"""

from __future__ import annotations

from ._utils import normalizar, tem_digitos_repetidos

_TAMANHO = 11


def _primeiro_dv(digitos: str) -> tuple[int, int]:
    """Calcula primeiro DV e retorna (dv, _dsc)."""
    total = sum(int(d) * w for d, w in zip(digitos[:9], range(9, 0, -1), strict=False))
    resto = total % 11
    if resto >= 10:
        return 0, 2
    return resto, 0


def _segundo_dv(digitos: str, dsc: int) -> int:
    total = sum(int(d) * w for d, w in zip(digitos[:9], range(1, 10), strict=False))
    resto = total % 11
    dv = resto - dsc
    if dv < 0:
        dv += 11
    if dv >= 10:
        return 0
    return dv


def validar_cnh(cnh: str | int) -> bool:
    """Valida uma CNH pelos dois dígitos verificadores."""
    cnh = normalizar(cnh)
    if len(cnh) != _TAMANHO or tem_digitos_repetidos(cnh):
        return False

    primeiro, dsc = _primeiro_dv(cnh)
    segundo = _segundo_dv(cnh, dsc)
    return cnh[-2:] == f"{primeiro}{segundo}"


def formatar_cnh(cnh: str | int) -> str:
    """Formata uma CNH no padrão ``XXX XXX XXX XX``."""
    cnh = normalizar(cnh)
    if len(cnh) != _TAMANHO:
        raise ValueError("CNH deve conter 11 dígitos para formatação.")
    return f"{cnh[:3]} {cnh[3:6]} {cnh[6:9]} {cnh[9:]}"


def gerar_cnh() -> str:
    """Gera uma CNH válida aleatória formatada."""
    import random

    base = [str(random.randint(0, 9)) for _ in range(9)]
    primeiro, dsc = _primeiro_dv("".join(base))
    base.append(str(primeiro))
    segundo = _segundo_dv("".join(base), dsc)
    base.append(str(segundo))
    cnh = "".join(base)
    return formatar_cnh(cnh)

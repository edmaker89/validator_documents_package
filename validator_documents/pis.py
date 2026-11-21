"""Validação e formatação de PIS/NIS/PASEP/NIT."""

from __future__ import annotations

from ._utils import normalizar, tem_digitos_repetidos

_TAMANHO = 11

_MULTIPLICADORES = (3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def validar_pis(pis: str | int) -> bool:
    """Valida um PIS/NIS/PASEP/NIT pelo dígito verificador."""
    pis = normalizar(pis)
    if len(pis) != _TAMANHO or tem_digitos_repetidos(pis):
        return False

    total = sum(int(d) * m for d, m in zip(pis[:10], _MULTIPLICADORES, strict=False))
    resto = total % 11
    digito = 0 if resto < 2 else 11 - resto
    return pis[-1] == str(digito)


def formatar_pis(pis: str | int) -> str:
    """Formata um PIS no padrão ``XXX.XXXXX.XX-X``."""
    pis = normalizar(pis)
    if len(pis) != _TAMANHO:
        raise ValueError("PIS deve conter 11 dígitos para formatação.")
    return f"{pis[:3]}.{pis[3:8]}.{pis[8:10]}-{pis[10:]}"


def gerar_pis() -> str:
    """Gera um PIS/NIS/PASEP/NIT válido aleatório formatado."""
    import random

    base = [str(random.randint(0, 9)) for _ in range(10)]
    total = sum(int(d) * m for d, m in zip(base, _MULTIPLICADORES, strict=False))
    resto = total % 11
    digito = 0 if resto < 2 else 11 - resto
    base.append(str(digito))
    pis = "".join(base)
    return formatar_pis(pis)

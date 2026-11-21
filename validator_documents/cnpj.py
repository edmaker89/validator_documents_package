"""Validação e formatação de CNPJ."""

from __future__ import annotations

from ._utils import normalizar, tem_digitos_repetidos

_TAMANHO = 14

_PESOS_DV_1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_PESOS_DV_2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def _digito_verificador(digitos: str, pesos: tuple[int, ...]) -> int:
    resto = sum(int(d) * p for d, p in zip(digitos, pesos, strict=False)) % 11
    return 0 if resto < 2 else 11 - resto


def validar_cnpj(cnpj: str | int) -> bool:
    """Valida um CNPJ pelos dígitos verificadores."""
    cnpj = normalizar(cnpj)
    if len(cnpj) != _TAMANHO or tem_digitos_repetidos(cnpj):
        return False

    primeiro = _digito_verificador(cnpj[:12], _PESOS_DV_1)
    segundo = _digito_verificador(cnpj[:13], _PESOS_DV_2)
    return cnpj[-2:] == f"{primeiro}{segundo}"


def formatar_cnpj(cnpj: str | int) -> str:
    """Formata um CNPJ no padrão ``XX.XXX.XXX/XXXX-XX``."""
    cnpj = normalizar(cnpj)
    if len(cnpj) != _TAMANHO:
        raise ValueError("CNPJ deve conter 14 dígitos para formatação.")
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def gerar_cnpj() -> str:
    """Gera um CNPJ válido aleatório formatado."""
    import random

    base = [str(random.randint(0, 9)) for _ in range(12)]
    primeiro = _digito_verificador("".join(base), _PESOS_DV_1)
    base.append(str(primeiro))
    segundo = _digito_verificador("".join(base), _PESOS_DV_2)
    base.append(str(segundo))
    cnpj = "".join(base)
    return formatar_cnpj(cnpj)

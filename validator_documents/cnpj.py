"""Validação e formatação de CNPJ (numérico e alfanumérico RFB).

Suporta o novo CNPJ alfanumérico da Receita Federal (Instrução Normativa
RFB nº 2.229/2024, vigente a partir de julho de 2026), onde as 12 primeiras
posições podem conter letras e dígitos, mantendo os dois dígitos
verificadores numéricos. O CNPJ numérico tradicional é um subconjunto
válido e continua funcionando.

Referência: serpro.gov.br — "Cálculo dos dígitos verificadores de CNPJ alfanumérico".
"""

from __future__ import annotations

import re

from ._utils import tem_digitos_repetidos

_ALNUM = re.compile(r"[^A-Z0-9]")

_TAMANHO = 14

_PESOS_DV_1 = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
_PESOS_DV_2 = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def normalizar_cnpj(cnpj: str | int) -> str:
    """Remove não-alfanuméricos e converte para maiúsculas.

    Diferente de :func:`validator_documents._utils.normalizar`, preserva as
    letras (A-Z), exigidas pelo CNPJ alfanumérico.
    """
    if isinstance(cnpj, int):
        return str(cnpj)
    if isinstance(cnpj, str):
        return _ALNUM.sub("", cnpj.upper())
    raise ValueError("O CNPJ deve ser uma string ou um número inteiro.")


def _valor_caractere(c: str) -> int:
    """Valor para cálculo do DV: dígito = valor numérico; letra = ord - 48.

    '0'..'9' → 0..9;  'A'..'Z' → 17..42 (subtrair 48 do código ASCII).
    """
    return ord(c) - 48


def _digito_verificador(caracteres: str, pesos: tuple[int, ...]) -> int:
    soma = sum(_valor_caractere(c) * p for c, p in zip(caracteres, pesos, strict=False))
    resto = soma % 11
    return 0 if resto < 2 else 11 - resto


def validar_cnpj(cnpj: str | int) -> bool:
    """Valida um CNPJ pelos dígitos verificadores (numérico ou alfanumérico).

    Regras:
    - 14 caracteres alfanuméricos após normalização;
    - os dois últimos caracteres (DVs) devem ser numéricos;
    - rejeita todos os caracteres iguais (ex.: ``AAAAAAAAAAAAAA``).
    """
    cnpj = normalizar_cnpj(cnpj)
    if len(cnpj) != _TAMANHO or tem_digitos_repetidos(cnpj):
        return False
    base, dv_informado = cnpj[:12], cnpj[12:]
    if not dv_informado.isdigit():
        return False
    primeiro = _digito_verificador(base, _PESOS_DV_1)
    segundo = _digito_verificador(base + str(primeiro), _PESOS_DV_2)
    return dv_informado == f"{primeiro}{segundo}"


def formatar_cnpj(cnpj: str | int) -> str:
    """Formata um CNPJ no padrão ``XX.XXX.XXX/XXXX-XX`` (numérico ou alfanumérico)."""
    cnpj = normalizar_cnpj(cnpj)
    if len(cnpj) != _TAMANHO:
        raise ValueError("CNPJ deve conter 14 caracteres alfanuméricos para formatação.")
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def gerar_cnpj() -> str:
    """Gera um CNPJ válido aleatório formatado (numérico, subconjunto do alfanumérico)."""
    import random

    base = [str(random.randint(0, 9)) for _ in range(12)]
    primeiro = _digito_verificador("".join(base), _PESOS_DV_1)
    base.append(str(primeiro))
    segundo = _digito_verificador("".join(base), _PESOS_DV_2)
    base.append(str(segundo))
    cnpj = "".join(base)
    return formatar_cnpj(cnpj)

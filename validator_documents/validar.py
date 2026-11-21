"""Despacho de validação por tipo e identificação de documento."""

from __future__ import annotations

import re
from typing import Literal

from . import cnh, cnpj, cpf, pis, placa, renavam, titulo_eleitoral
from .exceptions import DocumentoNaoIdentificado
from .placa import _PLACA_ANTIGA, _PLACA_MERCOSUL

TipoDocumento = Literal[
    "CPF",
    "CNPJ",
    "PIS",
    "TITULO_ELEITORAL",
    "CNH",
    "RENAVAM",
    "PLACA",
]

_VALIDADORES: dict[TipoDocumento, tuple[callable, callable, int | None]] = {
    "CPF": (cpf.validar_cpf, cpf.formatar_cpf, 11),
    "CNPJ": (cnpj.validar_cnpj, cnpj.formatar_cnpj, 14),
    "PIS": (pis.validar_pis, pis.formatar_pis, 11),
    "TITULO_ELEITORAL": (
        titulo_eleitoral.validar_titulo_eleitoral,
        titulo_eleitoral.formatar_titulo_eleitoral,
        12,
    ),
    "CNH": (cnh.validar_cnh, cnh.formatar_cnh, 11),
    "RENAVAM": (renavam.validar_renavam, renavam.formatar_renavam, 11),
    "PLACA": (placa.validar_placa, placa.formatar_placa, None),
}

_TAMANHO_PARA_TIPOS: dict[int, list[TipoDocumento]] = {}
for tipo, (_, _, tamanho) in _VALIDADORES.items():
    if tamanho is not None:
        _TAMANHO_PARA_TIPOS.setdefault(tamanho, []).append(tipo)


def validar_documento(
    valor: str | int, tipo: TipoDocumento | None = None, formatado: bool = False
) -> str | bool:
    """Valida um documento pelo tipo explícito ou tenta identificar automaticamente.

    Args:
        valor: Documento como string ou int.
        tipo: Tipo explícito (ex.: "CPF"). Se None, tenta identificar por comprimento.
        formatado: Se True, retorna o documento formatado; se False, retorna bool.

    Returns:
        bool (formatado=False) ou str formatado (formatado=True).

    Raises:
        DocumentoNaoIdentificado: Se tipo=None e o comprimento for ambíguo.
    """
    if tipo is None:
        tipo = identificar_documento(valor)

    validar_fn, formatar_fn, _ = _VALIDADORES[tipo]
    valido = validar_fn(valor)
    if formatado and valido:
        return formatar_fn(valor)
    return valido


def identificar_documento(valor: str | int) -> TipoDocumento:
    """Identifica o tipo de documento pelo comprimento alfanumérico.

    CNPJ alfanumérico (RFB) preserva letras A-Z nas 12 primeiras posições, então
    a contagem usa :func:`cnpj.normalizar_cnpj` (mantém A-Z) em vez de remover
    tudo que não é dígito.

    Raises:
        DocumentoNaoIdentificado: Se o comprimento for ambíguo ou não mapeado.
    """
    raw = str(valor).strip()
    # Placa: detecta por regex ANTES de normalizar (mantém letras)
    n = re.sub(r"[^A-Z0-9]", "", raw.upper())
    if _PLACA_ANTIGA.fullmatch(n) or _PLACA_MERCOSUL.fullmatch(n):
        return "PLACA"

    s = cnpj.normalizar_cnpj(valor)
    tamanho = len(s)

    candidatos = _TAMANHO_PARA_TIPOS.get(tamanho, [])
    if len(candidatos) == 1:
        return candidatos[0]
    if not candidatos:
        raise DocumentoNaoIdentificado(
            f"Comprimento {tamanho} não corresponde a nenhum tipo conhecido."
        )
    raise DocumentoNaoIdentificado(
        f"Comprimento {tamanho} é ambíguo: {', '.join(candidatos)}. "
        f"Use validar_documento(valor, tipo='...') explicitamente."
    )

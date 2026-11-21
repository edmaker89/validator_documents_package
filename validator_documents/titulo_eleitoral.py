"""Validação e formatação de Título Eleitoral.

Fonte normativa: Resolução TSE nº 23.659/2021, Art. 36 — 8 dígitos sequenciais,
2 dígitos de UF (01 a 28) e 2 dígitos verificadores, ambos por Módulo 11.

A ressalva histórica que transforma resto 0 em dígito 1 para SP/MG (01/02)
não consta na Resolução e, portanto, não é aplicada aqui.
"""

from __future__ import annotations

from ._utils import normalizar

_TAMANHO = 12

_PESOS_DV_1 = (2, 3, 4, 5, 6, 7, 8, 9)
_PESOS_DV_2 = (7, 8, 9)

_UFS_VALIDAS = tuple(f"{uf:02d}" for uf in range(1, 29))


def _modulo_11(digitos: list[int], pesos: tuple[int, ...]) -> int:
    resto = sum(d * p for d, p in zip(digitos, pesos, strict=False)) % 11
    return 0 if resto == 10 else resto


def validar_titulo_eleitoral(titulo: str | int) -> bool:
    """Valida um Título Eleitoral pelos dois dígitos verificadores."""
    titulo = normalizar(titulo)
    if len(titulo) != _TAMANHO:
        return False

    digitos = [int(d) for d in titulo]
    if titulo[8:10] not in _UFS_VALIDAS:
        return False

    primeiro = _modulo_11(digitos[0:8], _PESOS_DV_1)
    segundo = _modulo_11(digitos[8:10] + [primeiro], _PESOS_DV_2)
    return titulo[-2:] == f"{primeiro}{segundo}"


def formatar_titulo_eleitoral(titulo: str | int) -> str:
    """Formata um Título Eleitoral no padrão ``XXXX XXXX XXXX``."""
    titulo = normalizar(titulo)
    if len(titulo) != _TAMANHO:
        raise ValueError("Título Eleitoral deve conter 12 dígitos para formatação.")
    return f"{titulo[0:4]} {titulo[4:8]} {titulo[8:]}"


def gerar_titulo_eleitoral() -> str:
    """Gera um Título Eleitoral válido aleatório formatado.

    Usa UF aleatória (01 a 28) e segue a Resolução TSE 23.659/2021
    (sem exceção SP/MG para resto 0).
    """
    import random

    # 8 dígitos sequenciais aleatórios
    base = [str(random.randint(0, 9)) for _ in range(8)]
    # UF aleatória 01-28
    uf = f"{random.randint(1, 28):02d}"
    base.extend(list(uf))

    digitos = [int(d) for d in base]
    primeiro = _modulo_11(digitos[0:8], _PESOS_DV_1)
    segundo = _modulo_11(digitos[8:10] + [primeiro], _PESOS_DV_2)
    base.extend([str(primeiro), str(segundo)])

    titulo = "".join(base)
    return formatar_titulo_eleitoral(titulo)

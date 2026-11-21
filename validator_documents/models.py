"""Modelos Pydantic tipados para documentos brasileiros.

Cada modelo valida o documento na construção e expõe ``.valor`` (somente dígitos)
e ``.formatado`` (com máscara padrão).
"""

from typing import Self

from pydantic import BaseModel, ConfigDict, field_validator

from . import cnh, cnpj, cpf, pis, placa, renavam, titulo_eleitoral
from ._utils import normalizar
from .exceptions import DocumentoInvalido


class _DocumentoBase(BaseModel):
    """Base comum: normaliza, valida DV/formato, expõe formatado."""

    model_config = ConfigDict(frozen=True, str_strip_whitespace=True)

    valor: str

    _gerar_fn = None  # type: ignore[assignment]

    @field_validator("valor", mode="before")
    @classmethod
    def _normalizar(cls, v: str | int) -> str:
        return normalizar(v)

    @field_validator("valor")
    @classmethod
    def _validar(cls, v: str) -> str:
        if not cls._validar_fn(v):
            raise DocumentoInvalido(f"{cls.__name__} inválido: {v!r}")
        return v

    @property
    def formatado(self) -> str:
        return type(self)._formatar_fn(self.valor)

    @classmethod
    def gerar(cls) -> Self:
        """Gera uma instância válida aleatória do documento."""
        if cls._gerar_fn is None:
            raise NotImplementedError(f"{cls.__name__} não implementa geração.")
        valor = cls._gerar_fn()
        return cls(valor=valor)


class CPF(_DocumentoBase):
    """CPF — Cadastro de Pessoas Físicas."""

    _validar_fn = staticmethod(cpf.validar_cpf)
    _formatar_fn = staticmethod(cpf.formatar_cpf)
    _gerar_fn = staticmethod(cpf.gerar_cpf)


class CNPJ(_DocumentoBase):
    """CNPJ — Cadastro Nacional da Pessoa Jurídica (numérico e alfanumérico RFB)."""

    _validar_fn = staticmethod(cnpj.validar_cnpj)
    _formatar_fn = staticmethod(cnpj.formatar_cnpj)
    _gerar_fn = staticmethod(cnpj.gerar_cnpj)

    @field_validator("valor", mode="before")
    @classmethod
    def _normalizar(cls, v: str | int) -> str:
        """Normaliza preservando letras A-Z (CNPJ alfanumérico da RFB)."""
        return cnpj.normalizar_cnpj(v)


class PIS(_DocumentoBase):
    """PIS/NIS/PASEP/NIT."""

    _validar_fn = staticmethod(pis.validar_pis)
    _formatar_fn = staticmethod(pis.formatar_pis)
    _gerar_fn = staticmethod(pis.gerar_pis)


class TituloEleitoral(_DocumentoBase):
    """Título de Eleitor."""

    _validar_fn = staticmethod(titulo_eleitoral.validar_titulo_eleitoral)
    _formatar_fn = staticmethod(titulo_eleitoral.formatar_titulo_eleitoral)
    _gerar_fn = staticmethod(titulo_eleitoral.gerar_titulo_eleitoral)


class CNH(_DocumentoBase):
    """CNH — Carteira Nacional de Habilitação."""

    _validar_fn = staticmethod(cnh.validar_cnh)
    _formatar_fn = staticmethod(cnh.formatar_cnh)
    _gerar_fn = staticmethod(cnh.gerar_cnh)


class Renavam(_DocumentoBase):
    """RENAVAM — Registro Nacional de Veículos Automotores."""

    _validar_fn = staticmethod(renavam.validar_renavam)
    _formatar_fn = staticmethod(renavam.formatar_renavam)
    _gerar_fn = staticmethod(renavam.gerar_renavam)


class Placa(_DocumentoBase):
    """Placa veicular (padrão antigo ou Mercosul)."""

    _validar_fn = staticmethod(placa.validar_placa)
    _formatar_fn = staticmethod(placa.formatar_placa)
    _gerar_fn = staticmethod(placa.gerar_placa)

    @field_validator("valor", mode="before")
    @classmethod
    def _normalizar(cls, v: str | int) -> str:
        # Placa mantém letras — normalização diferente
        if isinstance(v, str):
            import re

            return re.sub(r"[^A-Z0-9]", "", v.upper())
        if isinstance(v, int):
            return str(v)
        raise DocumentoInvalido("Placa deve ser string ou inteiro.")

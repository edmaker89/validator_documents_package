"""validator-documents: Validação e formatação de documentos brasileiros.

Documentos suportados:
- CPF
- CNPJ
- PIS/NIS/PASEP/NIT
- Título Eleitoral
- CNH
- RENAVAM
- Placa veicular (antigo e Mercosul)
"""

from .cnh import formatar_cnh, gerar_cnh, validar_cnh
from .cnpj import formatar_cnpj, gerar_cnpj, validar_cnpj
from .cpf import formatar_cpf, gerar_cpf, validar_cpf
from .exceptions import DocumentoError, DocumentoInvalido, DocumentoNaoIdentificado
from .models import (
    CNH,
    CNPJ,
    CPF,
    PIS,
    Placa,
    Renavam,
    TituloEleitoral,
)
from .pis import formatar_pis, gerar_pis, validar_pis
from .placa import formatar_placa, gerar_placa, validar_placa
from .renavam import formatar_renavam, gerar_renavam, validar_renavam
from .titulo_eleitoral import (
    formatar_titulo_eleitoral,
    gerar_titulo_eleitoral,
    validar_titulo_eleitoral,
)
from .validar import TipoDocumento, identificar_documento, validar_documento

__all__ = [
    # Funções funcionais por tipo
    "validar_cpf",
    "formatar_cpf",
    "gerar_cpf",
    "validar_cnpj",
    "formatar_cnpj",
    "gerar_cnpj",
    "validar_pis",
    "formatar_pis",
    "gerar_pis",
    "validar_titulo_eleitoral",
    "formatar_titulo_eleitoral",
    "gerar_titulo_eleitoral",
    "validar_cnh",
    "formatar_cnh",
    "gerar_cnh",
    "validar_renavam",
    "formatar_renavam",
    "gerar_renavam",
    "validar_placa",
    "formatar_placa",
    "gerar_placa",
    # Despacho genérico
    "validar_documento",
    "identificar_documento",
    "TipoDocumento",
    # Modelos Pydantic
    "CPF",
    "CNPJ",
    "PIS",
    "TituloEleitoral",
    "CNH",
    "Renavam",
    "Placa",
    # Exceções
    "DocumentoError",
    "DocumentoInvalido",
    "DocumentoNaoIdentificado",
]

__version__ = "0.1.0"

"""Exceções do pacote :mod:`validator_documents`."""


class DocumentoError(ValueError):
    """Erro base para problemas de validação de documentos."""


class DocumentoInvalido(DocumentoError):
    """Documento inválido — comprimento, formato ou dígitos verificadores incorretos."""


class DocumentoNaoIdentificado(DocumentoError):
    """Não foi possível identificar o tipo do documento."""

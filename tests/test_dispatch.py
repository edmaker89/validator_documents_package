"""Testes do despacho genérico (validar_documento, identificar_documento)."""

import pytest

from validator_documents import (
    DocumentoNaoIdentificado,
    identificar_documento,
    validar_documento,
)


class TestValidarDocumento:
    def test_cpf_explicito(self):
        assert validar_documento("77548824181", tipo="CPF") is True
        assert validar_documento("775.488.241-81", tipo="CPF", formatado=True) == "775.488.241-81"

    def test_cnpj_explicito(self):
        assert validar_documento("67646869639155", tipo="CNPJ") is True

    def test_pis_explicito(self):
        assert validar_documento("43520735467", tipo="PIS") is True

    def test_titulo_explicito(self):
        assert validar_documento("763468501392", tipo="TITULO_ELEITORAL") is True

    def test_cnh_explicito(self):
        assert validar_documento("63677822635", tipo="CNH") is True

    def test_renavam_explicito(self):
        assert validar_documento("15021374471", tipo="RENAVAM") is True

    def test_placa_explicito(self):
        assert validar_documento("ABC1234", tipo="PLACA") is True

    def test_cpf_identificado(self):
        # 11 dígitos é ambíguo (CPF/PIS/CNH/RENAVAM) — deve levantar
        from validator_documents import DocumentoNaoIdentificado

        with pytest.raises(DocumentoNaoIdentificado):
            identificar_documento("77548824181")

    def test_cnpj_identificado(self):
        assert identificar_documento("67646869639155") == "CNPJ"
        assert identificar_documento("763468501392") == "TITULO_ELEITORAL"

    def test_placa_identificada(self):
        assert identificar_documento("ABC1234") == "PLACA"
        assert identificar_documento("ABC1D23") == "PLACA"

    def test_ambiguo_11_digitos_levanta(self):
        # CPF, PIS, CNH, RENAVAM são todos 11 dígitos
        with pytest.raises(DocumentoNaoIdentificado) as exc:
            identificar_documento("12345678901")
        assert "ambíguo" in str(exc.value)

    def test_comprimento_desconhecido_levanta(self):
        with pytest.raises(DocumentoNaoIdentificado):
            identificar_documento("12345")

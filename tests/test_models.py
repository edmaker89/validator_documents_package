"""Testes dos modelos Pydantic."""

import pytest
from pydantic import ValidationError

from validator_documents import (
    CNH,
    CNPJ,
    CPF,
    PIS,
    Placa,
    Renavam,
    TituloEleitoral,
)


class TestModeloCPF:
    def test_valido_string(self):
        c = CPF(valor="775.488.241-81")
        assert c.valor == "77548824181"
        assert c.formatado == "775.488.241-81"

    def test_valido_int(self):
        c = CPF(valor=77548824181)
        assert c.valor == "77548824181"

    def test_invalido_levanta_excecao(self):
        with pytest.raises(ValidationError):
            CPF(valor="11111111111")

    def test_dv_errado_levanta_excecao(self):
        with pytest.raises(ValidationError):
            CPF(valor="77548824180")


class TestModeloCNPJ:
    def test_valido_string(self):
        c = CNPJ(valor="67.646.869/6391-55")
        assert c.valor == "67646869639155"
        assert c.formatado == "67.646.869/6391-55"

    def test_valido_int(self):
        c = CNPJ(valor=67646869639155)
        assert c.valor == "67646869639155"

    def test_invalido(self):
        with pytest.raises(ValidationError):
            CNPJ(valor="11111111111111")


class TestModeloPIS:
    def test_valido(self):
        p = PIS(valor="435.20735.46-7")
        assert p.valor == "43520735467"
        assert p.formatado == "435.20735.46-7"

    def test_invalido(self):
        with pytest.raises(ValidationError):
            PIS(valor="11111111111")


class TestModeloTituloEleitoral:
    def test_valido(self):
        t = TituloEleitoral(valor="7634 6850 1392")
        assert t.valor == "763468501392"
        assert t.formatado == "7634 6850 1392"

    def test_invalido(self):
        with pytest.raises(ValidationError):
            TituloEleitoral(valor="111111111111")


class TestModeloCNH:
    def test_valido(self):
        c = CNH(valor="636 778 226 35")
        assert c.valor == "63677822635"
        assert c.formatado == "636 778 226 35"

    def test_invalido(self):
        with pytest.raises(ValidationError):
            CNH(valor="11111111111")


class TestModeloRenavam:
    def test_valido(self):
        r = Renavam(valor="1502137447-1")
        assert r.valor == "15021374471"
        assert r.formatado == "1502137447-1"

    def test_invalido(self):
        with pytest.raises(ValidationError):
            Renavam(valor="15021374470")


class TestModeloPlaca:
    def test_antigo(self):
        p = Placa(valor="abc1234")
        assert p.valor == "ABC1234"
        assert p.formatado == "ABC-1234"

    def test_mercosul(self):
        p = Placa(valor="ABC1D23")
        assert p.valor == "ABC1D23"
        assert p.formatado == "ABC1D23"

    def test_invalido(self):
        with pytest.raises(ValidationError):
            Placa(valor="ABC123")

    def test_letras_obrigatorias(self):
        with pytest.raises(ValidationError):
            Placa(valor="1231234")

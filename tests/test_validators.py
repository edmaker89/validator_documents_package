"""Testes dos validadores funcionais — fixtures verificadas contra validate-docbr."""

import pytest

from validator_documents import (
    CNH,
    CNPJ,
    CPF,
    PIS,
    Placa,
    Renavam,
    TituloEleitoral,
    formatar_cnh,
    formatar_cnpj,
    formatar_cpf,
    formatar_pis,
    formatar_placa,
    formatar_renavam,
    formatar_titulo_eleitoral,
    gerar_cnh,
    gerar_cnpj,
    gerar_cpf,
    gerar_pis,
    gerar_placa,
    gerar_renavam,
    gerar_titulo_eleitoral,
    validar_cnh,
    validar_cnpj,
    validar_cpf,
    validar_pis,
    validar_placa,
    validar_renavam,
    validar_titulo_eleitoral,
)

# Fixtures CPF (5 válidos do validate-docbr)
CPF_VALIDOS = [
    ("77548824181", "775.488.241-81"),
    ("01092692509", "010.926.925-09"),
    ("94438047943", "944.380.479-43"),
    ("04527488791", "045.274.887-91"),
    ("69621715016", "696.217.150-16"),
]
CPF_INVALIDOS = [
    "11111111111",  # dígitos repetidos
    "77548824180",  # DV errado
    "123456789",  # tamanho errado
]

# Fixtures CNPJ (5 válidos)
CNPJ_VALIDOS = [
    ("67646869639155", "67.646.869/6391-55"),
    ("14154590989172", "14.154.590/9891-72"),
    ("34709355803473", "34.709.355/8034-73"),
    ("39141313993692", "39.141.313/9936-92"),
    ("07302468923547", "07.302.468/9235-47"),
]
CNPJ_INVALIDOS = [
    "11111111111111",
    "67646869639154",
    "123456789",
]

# Fixtures CNPJ Alfanumérico (RFB — IN RFB nº 2.229/2024)
CNPJ_ALFANUMERICO_VALIDOS = [
    ("12ABC34501DE35", "12.ABC.345/01DE-35"),  # Exemplo oficial RFB
    ("95CR716532P858", "95.CR7.165/32P8-58"),
    ("KOZI2924181297", "KO.ZI2.924/1812-97"),
    ("74ZH760592C404", "74.ZH7.605/92C4-04"),
    ("16T31004654478", "16.T31.004/6544-78"),
    ("016Q57LG76O662", "01.6Q5.7LG/76O6-62"),
]
CNPJ_ALFANUMERICO_INVALIDOS = [
    "TE9A7033420235",  # DV errado
    "7L8U648F736183",  # DV errado
    "D62T278O686R51",  # DV errado
    "67556WJ9S29669",  # DV errado
    "H6C1653V3A2978",  # DV errado
    "AAAAAAAAAAAAAA",  # todos caracteres iguais
    "12ABC34501DE",  # tamanho errado (12)
    "12ABC34501DEA5",  # DV não numérico (letra)
]

# Fixtures PIS (5 válidos)
PIS_VALIDOS = [
    ("43520735467", "435.20735.46-7"),
    ("52499264560", "524.99264.56-0"),
    ("99688203131", "996.88203.13-1"),
    ("90797681456", "907.97681.45-6"),
    ("69422896990", "694.22896.99-0"),
]
PIS_INVALIDOS = [
    "11111111111",
    "43520735466",
    "123456789",
]

# Fixtures Título Eleitoral (5 válidos)
TITULO_VALIDOS = [
    ("763468501392", "7634 6850 1392"),
    ("762402470140", "7624 0247 0140"),
    ("424486511821", "4244 8651 1821"),
    ("309929381856", "3099 2938 1856"),
    ("754412112739", "7544 1211 2739"),
]
TITULO_INVALIDOS = [
    "111111111111",
    "763468501390",
    "123456789",
]

# Fixtures CNH (5 válidos)
CNH_VALIDOS = [
    ("63677822635", "636 778 226 35"),
    ("24762546350", "247 625 463 50"),
    ("59932477720", "599 324 777 20"),
    ("41185267325", "411 852 673 25"),
    ("58955214150", "589 552 141 50"),
]
CNH_INVALIDOS = [
    "11111111111",
    "63677822634",
    "123456789",
]

# Fixtures RENAVAM (5 válidos)
RENAVAM_VALIDOS = [
    ("15021374471", "1502137447-1"),
    ("30574500652", "3057450065-2"),
    ("84264015186", "8426401518-6"),
    ("66069054358", "6606905435-8"),
    ("17292179108", "1729217910-8"),
]
RENAVAM_INVALIDOS = [
    "15021374470",
    "123456789",
]

# Fixtures Placa
PLACA_VALIDAS = [
    ("ABC1234", "ABC-1234"),  # antigo
    ("abc1234", "ABC-1234"),  # case-insensitive
    ("ABC-1234", "ABC-1234"),  # já formatada
    ("ABC1D23", "ABC1D23"),  # Mercosul
    ("abc1d23", "ABC1D23"),  # Mercosul case-insensitive
]
PLACA_INVALIDAS = [
    "ABC123",  # curto
    "ABCD1234",  # 4 letras
    "1BC1234",  # começa com dígito
    "ABC12E4",  # padrão inválido
]


def _sem_zeros_esquerda(s: str) -> bool:
    """Verifica se a string numérica não tem zeros à esquerda."""
    return not s.startswith("0")


class TestCPF:
    @pytest.mark.parametrize("raw,formatado", CPF_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_cpf(raw) is True
        assert validar_cpf(formatado) is True
        if _sem_zeros_esquerda(raw):
            assert validar_cpf(int(raw)) is True

    @pytest.mark.parametrize("invalid", CPF_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_cpf(invalid) is False

    @pytest.mark.parametrize("raw,formatado", CPF_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_cpf(raw) == formatado
        if _sem_zeros_esquerda(raw):
            assert formatar_cpf(int(raw)) == formatado


class TestCNPJAlfanumerico:
    """Testes para CNPJ alfanumérico (RFB IN 2.229/2024)."""

    @pytest.mark.parametrize("raw,formatado", CNPJ_ALFANUMERICO_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_cnpj(raw) is True
        assert validar_cnpj(formatado) is True

    @pytest.mark.parametrize("invalid", CNPJ_ALFANUMERICO_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_cnpj(invalid) is False

    @pytest.mark.parametrize("raw,formatado", CNPJ_ALFANUMERICO_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_cnpj(raw) == formatado

    def test_modelo_pydantic(self):
        cnpj = CNPJ(valor="12ABC34501DE35")
        assert cnpj.valor == "12ABC34501DE35"
        assert cnpj.formatado == "12.ABC.345/01DE-35"

    def test_identificar_documento(self):
        from validator_documents import identificar_documento

        assert identificar_documento("12ABC34501DE35") == "CNPJ"
        assert identificar_documento("12.ABC.345/01DE-35") == "CNPJ"


class TestCNPJ:
    @pytest.mark.parametrize("raw,formatado", CNPJ_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_cnpj(raw) is True
        assert validar_cnpj(formatado) is True
        if _sem_zeros_esquerda(raw):
            assert validar_cnpj(int(raw)) is True

    @pytest.mark.parametrize("invalid", CNPJ_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_cnpj(invalid) is False

    @pytest.mark.parametrize("raw,formatado", CNPJ_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_cnpj(raw) == formatado
        if _sem_zeros_esquerda(raw):
            assert formatar_cnpj(int(raw)) == formatado


class TestPIS:
    @pytest.mark.parametrize("raw,formatado", PIS_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_pis(raw) is True
        assert validar_pis(formatado) is True
        if _sem_zeros_esquerda(raw):
            assert validar_pis(int(raw)) is True

    @pytest.mark.parametrize("invalid", PIS_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_pis(invalid) is False

    @pytest.mark.parametrize("raw,formatado", PIS_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_pis(raw) == formatado
        if _sem_zeros_esquerda(raw):
            assert formatar_pis(int(raw)) == formatado


class TestTituloEleitoral:
    @pytest.mark.parametrize("raw,formatado", TITULO_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_titulo_eleitoral(raw) is True
        assert validar_titulo_eleitoral(formatado) is True
        if _sem_zeros_esquerda(raw):
            assert validar_titulo_eleitoral(int(raw)) is True

    @pytest.mark.parametrize("invalid", TITULO_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_titulo_eleitoral(invalid) is False

    @pytest.mark.parametrize("raw,formatado", TITULO_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_titulo_eleitoral(raw) == formatado
        if _sem_zeros_esquerda(raw):
            assert formatar_titulo_eleitoral(int(raw)) == formatado


class TestCNH:
    @pytest.mark.parametrize("raw,formatado", CNH_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_cnh(raw) is True
        assert validar_cnh(formatado) is True
        if _sem_zeros_esquerda(raw):
            assert validar_cnh(int(raw)) is True

    @pytest.mark.parametrize("invalid", CNH_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_cnh(invalid) is False

    @pytest.mark.parametrize("raw,formatado", CNH_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_cnh(raw) == formatado
        if _sem_zeros_esquerda(raw):
            assert formatar_cnh(int(raw)) == formatado


class TestRENAVAM:
    @pytest.mark.parametrize("raw,formatado", RENAVAM_VALIDOS)
    def test_validar(self, raw, formatado):
        assert validar_renavam(raw) is True
        assert validar_renavam(formatado) is True
        if _sem_zeros_esquerda(raw):
            assert validar_renavam(int(raw)) is True

    @pytest.mark.parametrize("invalid", RENAVAM_INVALIDOS)
    def test_invalidar(self, invalid):
        assert validar_renavam(invalid) is False

    @pytest.mark.parametrize("raw,formatado", RENAVAM_VALIDOS)
    def test_formatar(self, raw, formatado):
        assert formatar_renavam(raw) == formatado
        if _sem_zeros_esquerda(raw):
            assert formatar_renavam(int(raw)) == formatado


class TestPlaca:
    @pytest.mark.parametrize("raw,formatado", PLACA_VALIDAS)
    def test_validar(self, raw, formatado):
        assert validar_placa(raw) is True
        assert validar_placa(raw.upper()) is True

    @pytest.mark.parametrize("invalid", PLACA_INVALIDAS)
    def test_invalidar(self, invalid):
        assert validar_placa(invalid) is False

    @pytest.mark.parametrize("raw,formatado", PLACA_VALIDAS)
    def test_formatar(self, raw, formatado):
        assert formatar_placa(raw) == formatado


class TestGerar:
    """Testes das funções de geração — validam que o gerado é válido."""

    def test_gerar_cpf(self):
        for _ in range(10):
            cpf = gerar_cpf()
            assert validar_cpf(cpf) is True
            assert formatar_cpf(cpf) == cpf

    def test_gerar_cnpj(self):
        for _ in range(10):
            cnpj = gerar_cnpj()
            assert validar_cnpj(cnpj) is True
            assert formatar_cnpj(cnpj) == cnpj

    def test_gerar_pis(self):
        for _ in range(10):
            pis = gerar_pis()
            assert validar_pis(pis) is True
            assert formatar_pis(pis) == pis

    def test_gerar_titulo_eleitoral(self):
        for _ in range(10):
            titulo = gerar_titulo_eleitoral()
            assert validar_titulo_eleitoral(titulo) is True
            assert formatar_titulo_eleitoral(titulo) == titulo

    def test_gerar_cnh(self):
        for _ in range(10):
            cnh = gerar_cnh()
            assert validar_cnh(cnh) is True
            assert formatar_cnh(cnh) == cnh

    def test_gerar_renavam(self):
        for _ in range(10):
            renavam = gerar_renavam()
            assert validar_renavam(renavam) is True
            assert formatar_renavam(renavam) == renavam

    def test_gerar_placa_antigo(self):
        for _ in range(10):
            placa = gerar_placa(mercosul=False)
            assert validar_placa(placa) is True
            assert formatar_placa(placa) == placa
            assert "-" in placa  # antigo tem hífen

    def test_gerar_placa_mercosul(self):
        for _ in range(10):
            placa = gerar_placa(mercosul=True)
            assert validar_placa(placa) is True
            assert formatar_placa(placa) == placa
            assert "-" not in placa  # Mercosul sem hífen


class TestModelGerar:
    """Testes do método .gerar() dos modelos Pydantic."""

    def test_cpf_gerar(self):
        for _ in range(10):
            cpf = CPF.gerar()
            assert validar_cpf(cpf.valor) is True
            assert cpf.formatado == formatar_cpf(cpf.valor)

    def test_cnpj_gerar(self):
        for _ in range(10):
            cnpj = CNPJ.gerar()
            assert validar_cnpj(cnpj.valor) is True
            assert cnpj.formatado == formatar_cnpj(cnpj.valor)

    def test_pis_gerar(self):
        for _ in range(10):
            pis = PIS.gerar()
            assert validar_pis(pis.valor) is True
            assert pis.formatado == formatar_pis(pis.valor)

    def test_titulo_eleitoral_gerar(self):
        for _ in range(10):
            titulo = TituloEleitoral.gerar()
            assert validar_titulo_eleitoral(titulo.valor) is True
            assert titulo.formatado == formatar_titulo_eleitoral(titulo.valor)

    def test_cnh_gerar(self):
        for _ in range(10):
            cnh = CNH.gerar()
            assert validar_cnh(cnh.valor) is True
            assert cnh.formatado == formatar_cnh(cnh.valor)

    def test_renavam_gerar(self):
        for _ in range(10):
            renavam = Renavam.gerar()
            assert validar_renavam(renavam.valor) is True
            assert renavam.formatado == formatar_renavam(renavam.valor)

    def test_placa_gerar_antigo(self):
        for _ in range(10):
            placa = Placa.gerar()
            assert validar_placa(placa.valor) is True
            assert placa.formatado == formatar_placa(placa.valor)
            assert "-" in placa.formatado  # formato antigo tem hífen

    def test_placa_gerar_mercosul(self):
        # Placa.gerar() chama gerar_placa() sem parâmetros (padrão antigo)
        # Testamos mercosul via função direta
        from validator_documents import gerar_placa

        for _ in range(10):
            placa_str = gerar_placa(mercosul=True)
            placa = Placa(valor=placa_str)
            assert validar_placa(placa.valor) is True
            assert placa.formatado == formatar_placa(placa.valor)
            assert "-" not in placa.valor

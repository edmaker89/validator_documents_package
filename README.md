# validator-documents

[![PyPI version](https://img.shields.io/pypi/v/validator-documents.svg)](https://pypi.org/project/validator-documents/)
[![Python versions](https://img.shields.io/pypi/pyversions/validator-documents.svg)](https://pypi.org/project/validator-documents/)
[![License](https://img.shields.io/pypi/l/validator-documents.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/edmaker89/validator_documents_package/actions/workflows/ci.yml/badge.svg)](https://github.com/edmaker89/validator_documents_package/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/edmaker89/validator_documents_package/main/coverage-badge.json)](https://github.com/edmaker89/validator_documents_package/actions/workflows/ci.yml)

Validação e formatação de documentos brasileiros com tipagem Pydantic v2.

**Documentos suportados:**
- CPF (Cadastro de Pessoas Físicas)
- CNPJ (Cadastro Nacional da Pessoa Jurídica)
- PIS/NIS/PASEP/NIT
- Título Eleitoral
- CNH (Carteira Nacional de Habilitação)
- RENAVAM (Registro Nacional de Veículos Automotores)
- Placa veicular (padrão antigo e Mercosul)

## Instalação

```bash
pip install validator-documents
```

Requer Python ≥ 3.10.

## Uso rápido

### Funções funcionais (por tipo)

```python
from validator_documents import (
    validar_cpf,
    formatar_cpf,
    validar_cnpj,
    formatar_cnpj,
    validar_pis,
    formatar_pis,
    validar_titulo_eleitoral,
    formatar_titulo_eleitoral,
    validar_cnh,
    formatar_cnh,
    validar_renavam,
    formatar_renavam,
    validar_placa,
    formatar_placa,
)

# Validação
validar_cpf("775.488.241-81")  # True
validar_cnpj("67.646.869/6391-55")  # True
validar_cnpj("12.ABC.345/01DE-35")  # True (CNPJ alfanumérico RFB)
validar_pis("435.20735.46-7")  # True
validar_titulo_eleitoral("7634 6850 1392")  # True
validar_cnh("636 778 226 35")  # True
validar_renavam("1502137447-1")  # True
validar_placa("ABC1234")  # True (antigo)
validar_placa("ABC1D23")  # True (Mercosul)

# Formatação
formatar_cpf("77548824181")  # "775.488.241-81"
formatar_cnpj("67646869639155")  # "67.646.869/6391-55"
formatar_placa("abc1234")  # "ABC-1234"
```

### Geração de documentos válidos (para testes/fixtures)

```python
from validator_documents import (
    gerar_cpf,
    gerar_cnpj,
    gerar_pis,
    gerar_titulo_eleitoral,
    gerar_cnh,
    gerar_renavam,
    gerar_placa,
)

# Funções funcionais
cpf = gerar_cpf()  # "775.488.241-81"
cnpj = gerar_cnpj()  # "67.646.869/6391-55"
pis = gerar_pis()  # "435.20735.46-7"
titulo = gerar_titulo_eleitoral()  # "7634 6850 1392"
cnh = gerar_cnh()  # "636 778 226 35"
renavam = gerar_renavam()  # "1502137447-1"
placa_antigo = gerar_placa()  # "ABC-1234"
placa_mercosul = gerar_placa(True)  # "ABC1D23"
```

### Modelos Pydantic com `.gerar()`

```python
from validator_documents import CPF, CNPJ, PIS, TituloEleitoral, CNH, Renavam, Placa

# Classe método .gerar() retorna instância tipada válida
cpf = CPF.gerar()
cpf.valor  # "77548824181" (apenas dígitos)
cpf.formatado  # "775.488.241-81"

cnpj = CNPJ.gerar()
pis = PIS.gerar()
# ... idem para TituloEleitoral, CNH, Renavam, Placa

# Placa Mercosul via função + modelo
from validator_documents import gerar_placa

placa_mercosul = Placa(valor=gerar_placa(mercosul=True))
placa_mercosul.formatado  # "ABC1D23" (sem hífen)
```

### Despacho genérico

```python
from validator_documents import validar_documento, identificar_documento

# Tipo explícito (recomendado para evitar ambiguidade de 11 dígitos)
validar_documento("77548824181", tipo="CPF")  # True
validar_documento("775.488.241-81", tipo="CPF", formatado=True)  # "775.488.241-81"

# Identificação automática (funciona apenas quando não ambíguo)
identificar_documento("77548824181")  # "CPF"
identificar_documento("ABC1234")  # "PLACA"

# 11 dígitos é ambíguo (CPF/PIS/CNH/RENAVAM) — lança DocumentoNaoIdentificado
identificar_documento("12345678901")  # Exception: use tipo explícito
```

### Modelos Pydantic (tipagem estática)

```python
from validator_documents import CPF, CNPJ, PIS, TituloEleitoral, CNH, Renavam, Placa

cpf = CPF(valor="775.488.241-81")
cpf.valor  # "77548824181" (apenas dígitos)
cpf.formatado  # "775.488.241-81"

# Valida na construção — levanta DocumentoInvalido se inválido
try:
    CPF(valor="11111111111")
except DocumentoInvalido as e:
    print(e)  # "CPF inválido: '11111111111'"
```

### Tipos de exceção

```python
from validator_documents import DocumentoInvalido, DocumentoNaoIdentificado

# DocumentoInvalido — DV/formato incorreto
# DocumentoNaoIdentificado — identificação automática ambígua
```

## Compatibilidade e decisões de design

| Documento | Tamanho | DV? | Padrão de formatação |
|-----------|---------|-----|----------------------|
| CPF       | 11      | Sim | `XXX.XXX.XXX-XX`     |
| CNPJ      | 14      | Sim | `XX.XXX.XXX/XXXX-XX` |
| CNPJ (alfanumérico) | 14 alfanum. | Sim | `XX.XXX.XXX/XXXX-XX` |
| PIS       | 11      | Sim | `XXX.XXXXX.XX-X`     |
| Título Eleitoral | 12 | Sim | `XXXX XXXX XXXX`    |
| CNH       | 11      | Sim | `XXX XXX XXX XX`     |
| RENAVAM   | 11      | Sim | `XXXXXXXXXX-X`       |
| Placa     | 7 alfanum. | Não | `ABC-1234` (antigo) / `ABC1D23` (Mercosul) |

**Decisões relevantes:**
- **Identificação automática por comprimento** é limitada: 11 dígitos corresponde a CPF, PIS, CNH e RENAVAM — nesses casos, use `validar_documento(valor, tipo="...")` explícito.
- **Título Eleitoral**: segue a Resolução TSE 23.659/2021 (sem exceção SP/MG onde resto 0 vira 1). Se seu caso de uso exigir a exceção legada, abra uma issue.
- **Placa Mercosul**: formatada sem hífen (`ABC1D23`), conforme padrão oficial.
- **Dígitos repetidos** (ex.: `111.111.111-11`) são rejeitados para CPF, CNPJ, PIS e CNH.
- **CNPJ alfanumérico** (IN RFB nº 2.229/2024): suporta letras A-Z nas 12 primeiras posições; os dois dígitos verificadores permanecem numéricos; o CNPJ numérico tradicional continua válido como subconjunto.

## Desenvolvimento

```bash
# Instala dependências de dev
pip install ".[dev]"

# Lint
ruff check .

# Format
ruff format .

# Testes + cobertura
pytest -q
```

## Licença

MIT — veja [LICENSE](LICENSE).
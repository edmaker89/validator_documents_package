# Evolução do Produto — validator-documents

## Resumo

Transformação do pacote original `validator_docs` (apenas CPF/CNPJ, sem tipagem, setup.py legado) em `validator-documents` — biblioteca moderna, tipada, testada e pronta para PyPI, suportando 7 tipos de documentos brasileiros.

---

## Estado Original (antes)

| Aspecto | Detalhes |
|---------|----------|
| Nome do pacote | `validador_docs` (setup.py) / `validator_docs` (import) |
| Documentos | CPF, CNPJ apenas |
| Tipagem | Nenhuma (type hints parciais em `validador.py`) |
| Build | `setup.py` + `pytest-runner` (legacy) |
| CI/CD | Apenas workflow de publish (sem lint/test gate) |
| Testes | 1 arquivo, fixtures fictícias, sem cobertura |
| README | Básico, sem badges |
| Licença | Mencionada mas arquivo `LICENSE` ausente |
| Python | `>=3.12` (muito restritivo) |
| Bugs conhecidos | CPF/CNPJ aceitavam dígitos repetidos (`111.111.111-11` válido) |
| `identificar_documento` | Por comprimento apenas; não escala |

---

## Estado Atual (v0.1.0)

| Aspecto | Detalhes |
|---------|----------|
| Nome distribuição | `validator-documents` (PyPI) |
| Nome importação | `validator_documents` |
| Documentos | **7**: CPF, CNPJ, PIS, Título Eleitoral, CNH, RENAVAM, Placa |
| Tipagem | **Pydantic v2** — 7 modelos (`CPF`, `CNPJ`, `PIS`, `TituloEleitoral`, `CNH`, `Renavam`, `Placa`) + API funcional |
| Build | `pyproject.toml` + `hatchling` (PEP 621) |
| Testes | 3 arquivos, **138 testes**, fixtures validadas contra `validate-docbr` (referência), cobertura **95.6%** |
| README | Badges, exemplos, tabela de decisões |
| Licença | MIT — arquivo `LICENSE` presente |
| Qualidade | `ruff` formatado, sem warnings |

---

## Decisões Técnicas Tomadas

| # | Decisão | Justificativa | Status |
|---|---------|---------------|--------|
| 1 | Renomear distribuição para `validator-documents` e import para `validator_documents` | Alinha com pedido do usuário (`pip install validator-documents`) e convenção PyPI (kebab-case → snake_case) | ✅ Feito |
| 2 | Pydantic v2 (não v1) | Atual, performático, API moderna (`field_validator`, `ConfigDict`) | ✅ Feito |
| 3 | Python `>=3.10` | Pydantic v2 suporta 3.8+; 3.10 evita EOL próximo e permite `str | int` | ✅ Feito |
| 4 | Rejeitar dígitos repetidos em CPF, CNPJ, PIS, CNH | Segurança: `111.111.111-11` passava DV mas é inválido na prática | ✅ Feito |
| 5 | Título Eleitoral **sem** exceção SP/MG (resto 0 → dígito 1) | Segue Resolução TSE 23.659/2021 e `validate-docbr` (referência moderna) | ✅ Feito |
| 6 | Placa Mercosul formatada sem hífen (`ABC1D23`) | Padrão oficial do Mercosul | ✅ Feito |
| 7 | `identificar_documento` levanta `DocumentoNaoIdentificado` para 11 dígitos | Ambiguidade real: CPF/PIS/CNH/RENAVAM têm 11 dígitos — auto-detecção por comprimento não funciona mais | ✅ Feito |
| 8 | `int` como entrada perde zeros à esquerda — testes só usam `int` quando não há zeros à esquerda | CPF/CNPJ/PIS/Título/CNH/RENAVAM podem começar com 0; `int("0123...")` → `123...` quebra validação | ✅ Documentado |

---

## Gaps / Decisões Pendentes (resolvidas)

| # | Gap | Decisão Final |
|---|-----|---------------|
| **1** | **Título Eleitoral: exceção SP/MG** | ✅ **Mantido sem exceção** — Resolução TSE 23.659/2021, Art. 36 não prevê a exceção SP/MG; a exceção era prática legada não normatizada. `validate-docbr` não implementa (issue #70). Se necessário, pode ser adicionado parâmetro opcional `legado=True` futuramente. |
| **2** | **Placa: formatação Mercosul** | ✅ **Sem hífen** — Recebe com/sem hífen, normaliza (remove não-alfanumérico), valida regex, formata sem hífen (`ABC1D23`). Padrão oficial Mercosul. |
| **3** | **Python `>=3.10` vs `>=3.9` vs `>=3.11`** | ✅ **Mantido `>=3.10`** — Piso 3.10 garante `str | int` nativo; CI testa 3.10–3.13; 3.9 ainda suportado até 2025-10 mas não como piso. |
| **4** | **Nome no PyPI: `validator-documents`** | ⏳ **Sua decisão** — Nome livre (404), pronto para `git tag v0.1.0 && git push --tags`. |
| **5** | **API `validar_doc` legada** | ✅ **Removida** — clean cutover; `validar_documento` exige tipo explícito para 11 dígitos. Breaking change aceitável em 0.x não publicado. |
| **6** | **Cobertura de testes** | ✅ **95.11%** — com testes de geração incluídos (8 novos testes `TestGerar`). |

---

## Novidades Adicionadas (pós-decisão)

| Item | Descrição |
|------|-----------|
| **Métodos `gerar_*`** | 7 funções: `gerar_cpf()`, `gerar_cnpj()`, `gerar_pis()`, `gerar_titulo_eleitoral()`, `gerar_cnh()`, `gerar_renavam()`, `gerar_placa(mercosul=bool)` — geram documentos válidos aleatórios formatados, ideais para testes/fixtures. |
| **Método `.gerar()` nos modelos** | Todos os 7 modelos Pydantic expõem `cls.gerar()` (ex.: `CPF.gerar()`, `CNPJ.gerar()`) — retorna instância válida tipada. |
| **Testes de geração** | `TestGerar` (8 testes) + `TestModelGerar` (8 testes) validando que cada documento gerado passa na validação e formatação. |
| **Cobertura final** | **95.6%** (acima do mínimo 90%). |
| **Placa Mercosul** | Recebe com/sem hífen, normaliza (remove não-alfanumérico), valida regex, formata **sem hífen** (`ABC1D23`). |

---

## Explicação: Título Eleitoral SP/MG (Gap #1)

A "exceção SP/MG" refere-se a uma prática legada onde, no cálculo do 1º DV do Título Eleitoral, se o resto da divisão por 11 fosse 0 **e** a UF fosse São Paulo (01) ou Minas Gerais (02), o dígito verificador seria forçado a 1 (em vez de 0).

**Por que NÃO implementamos:**
1. **Resolução TSE 23.659/2021, Art. 36** define o algoritmo puro (Módulo 11, resto 10 → 0, sem menção a exceção por UF).
2. **`validate-docbr`** (biblioteca referência mantida por Álvaro Justen) **não implementa** a exceção — ver issue #70 do repositório.
3. A exceção era uma interpretação administrativa antiga, não normatizada em resolução vigente.
4. Implementar a exceção geraria **falsos negativos** para títulos válidos emitidos sob a norma atual.

**Se você precisar da exceção legada** (ex.: validar base antiga que a usa), podemos adicionar parâmetro opcional `legado=True` em `validar_titulo_eleitoral` e `TituloEleitoral`. Avise se for o caso.

---

## Próximos Passos Sugeridos (v0.2+)

1. **CLI**: `validator-documents validar --tipo CPF "123.456.789-09"`
2. ~~Método `.gerar()` nos modelos Pydantic (ex.: `CPF.gerar()`).~~ ✅ **Feito** — todos os 7 modelos expõem `cls.gerar()`.
3. ~~**Suporte a CNPJ alfanumérico** (nova formatação RFB).~~ ✅ **Feito** — IN RFB nº 2.229/2024 implementada (validação, formatação, modelo Pydantic, identificação automática).
4. **Documentação Sphinx** + publicação no ReadTheDocs.
5. **Benchmarks** de performance vs `validate-docbr` / `cpf-cnpj-validator`.
6. **Schema JSON** dos modelos para integração com outros sistemas.
---

## Como Discutir os Gaps

Se você quiser discutir qualquer gap acima:
1. Abra uma issue no GitHub com o número do gap (ex.: "Gap #1: Título Eleitoral SP/MG")
2. Ou responda aqui com sua preferência e eu aplico a alteração.

O modo **brainstorm (egm-brainstorm)** **não está carregado** nesta sessão — as decisões acima foram tomadas com base em evidências (referências normativas, `validate-docbr`, convenções PyPI). Se preferir uma sessão de brainstorm estruturada para algum gap, avise e eu invoco a skill.
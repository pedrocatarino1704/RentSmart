# RentSmart – Sistema de Orçamento de Locação (R.M Imóveis)

Aplicação em Python (Programação Orientada a Objetos) que calcula o orçamento mensal de locação de
apartamentos, casas e estúdios, apresenta um resumo detalhado e gera um CSV com a projeção dos 12 primeiros meses.

## Requisitos
- Python 3.9 ou superior (somente biblioteca padrão, não há dependências para instalar)

## Como executar
```bash
git clone <URL-DO-SEU-REPOSITORIO>
cd rentsmart
python main.py
```
Responda às perguntas no terminal. Ao final, o orçamento é exibido e o arquivo `projecao_12_meses.csv` é criado.

## Como executar os testes
```bash
python -m unittest discover -s tests -t . -v
```

## Regras implementadas
| Item | Regra |
|---|---|
| Aluguel-base | Apartamento R$ 700 · Casa R$ 900 · Estúdio R$ 1.200 |
| 2 quartos | Apartamento +R$ 200 · Casa +R$ 250 |
| Garagem (casa/apto) | +R$ 300 por mês (1 vaga) |
| Estúdio | Pacote de 2 vagas R$ 250 + R$ 60 por vaga adicional |
| Desconto | Apartamento sem crianças: 5% sobre o aluguel já com adicionais |
| Taxa contratual | R$ 2.000, parcelável em 1 a 5x, exibida separadamente do aluguel |

### Decisões de projeto
- Estacionamento do estúdio é opcional (0 vagas = nenhuma). Com 1 ou 2 vagas paga-se o pacote (R$ 250).
- O desconto de 5% incide sobre aluguel-base + adicional de quartos + garagem.
- As parcelas da taxa são cobradas nos primeiros meses do contrato; a última parcela absorve a diferença de centavos.
- Valores monetários usam `Decimal` para evitar erros de ponto flutuante.

## Estrutura do projeto
```
main.py                  # ponto de entrada
rentsmart/
  imoveis.py             # Imovel (abstrata), Apartamento, Casa, Estudio
  orcamento.py           # TaxaContratual e Orcamento
  projecao.py            # geração do CSV
  interface.py           # entrada de dados e validação
tests/test_rentsmart.py  # testes automatizados
exemplo_projecao_12_meses.csv
```

## Formato do CSV
Separador `;` e vírgula decimal (abre direto no Excel em português). Colunas: `mes;aluguel;taxa_contratual;total_mes`.

## Autor
[SEU NOME] – [CURSO / INSTITUIÇÃO]

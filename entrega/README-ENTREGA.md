# Defeitos corrigidos

1. **Cálculo de câmbio**
   **Causa raiz:** O código dividia o valor pela taxa de câmbio em vez de multiplicar e convertia o resultado para float, e no próprio README.md já é dito que "Use Decimal, nunca float, no dinheiro."

2. **Cálculo de dias**
   **Causa raiz:** O cálculo subtraía apenas o dia do mês, resultando em valores negativos ou incorretos em estadias que viram o mês.

3. **Filtro de status**
   **Causa raiz:** A regra barrava apenas reservas "CANCELLED", permitindo que reservas "NO_SHOW" entrassem na contagem de faturamento e das noites.

4. **Ordenação do ranking**
   **Causa raiz:** A lista top_hotels estava ordenada de forma crescente pelo valor total, quando o esperado era ordem decrescente pelo valor com desempate ascendente pelo id do hotel.

5. **Leitura das reservas do CSV**
   **Causa raiz:** Havia um if interrompendo a leitura do arquivo na linha 200, descartando os últimos 100 registros do reserva_hoteis.csv.

# Como investiguei

- Rodei o pytest no começo para identificar os erros (câmbio, diárias, status e ranking). Após corrigir um por um, rodei o pytest novamente e tive a confirmação de que havia corrigido da maneira certa.
- Rodei a CLI usando o data/exemplo-validacao.csv como entrada e comparei o JSON gerado com os valores do README. Notei que estava certo.
- Depois, rodei novamente a CLI porém agora passando o data/reservas_hoteis.csv como entrada. Notei que o report.json mostrava apenas 200 reservas, quando o esperado era 300. Assim, encontrei o corte na linha 200 do repositório CSV, que passava batido na amostra de 12 linhas.
- Adicionei o teste tests/test_adicional_top_hotel.py para cobrir o desempate pelo id do hotel quando há empate de valor no ranking.

## Como validar

Com o ambiente virtual ativo e as dependências instaladas:

```bash
# Rodar os testes (5 originais + 1 adicional):
pytest -v

# Gerar o relatório da amostra de validação
python -m onfly_report --input data/exemplo-validacao.csv --rates data/taxas_cambio.csv --output output/exemplo.json

# Gerar o relatório completo das 300 reservas
python -m onfly_report --input data/reservas_hoteis.csv --rates data/taxas_cambio.csv --output output/report.json
```

## Resultado

* **Testes:** 6 passed no pytest.
* **Amostra (output/exemplo.json):** Valores do resumo, agrupamento por mês e ranking batendo com o gabarito do README.md.
* **Base principal (output/report.json):** Todas as 300 reservas lidas (235 confirmadas, 31 canceladas e 34 no-show), somando 1347 noites, 396170.00 BRL de faturamento e diária média de 294.11 BRL.
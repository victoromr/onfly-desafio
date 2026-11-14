# Declaração de Uso de IA

- **Ferramenta utilizada:** Google Gemini
- **Log da sessão:** entrega/uso-de-ia/sessao.md

## O que eu fiz

- Analisei o código e identifiquei a causa raiz dos 5 defeitos (câmbio, cálculo de dias, filtro de status, ordenação do ranking e a leitura do CSV).
- Implementei todas as correções nos arquivos de "src/onfly_report/".
- Criei o teste adicional "tests/test_adicional_top_hotel.py" para validar o desempate pelo id do hotel.
- Rodei a suíte do pytest e gerei os arquivos "output/exemplo.json" e "output/report.json".

## Como usei a IA

Como minha experiência principal é em C#, usei o Gemini para tirar dúvidas de sintaxe do Python e para fazer uma segunda conferência nos números do relatório final:

- **Comparação de sintaxe (C# para Python):** Tirei dúvidas sobre subtração entre datas ("date" e ".days", parecido com o "TimeSpan.Days" no C#) e sobre o funcionamento de construtores.
- **Conferência das contas:** Pedi para somar os valores mensais do "output/report.json" gerado e validar se batiam com o total geral e com a diária média.
# Sessão de Uso de IA

## Interação 1

### Prompt

def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos."""
    return (checkout.day - checkin.day) * rooms

// em c#, o uso de um .day seria desnecessário porque o código já sabe que é do tipo data. em python é a mesma coisa? 

### Resposta

Sim — em Python você também deve subtrair as datas diretamente, mas, assim como no C#, a subtração entre duas datas não retorna um número inteiro direto, e sim um objeto de intervalo de tempo (`timedelta`), do qual você extrai `.days` (no plural).

Usar `.day` (no singular) em cada data como está no seu código causa um **bug na virada de mês**: `.day` retorna apenas o dia do calendário (de 1 a 31). Se o check-in for dia 30 e o check-out for dia 2 do mês seguinte, a conta fará `2 - 30 = -28` diárias.

A forma correta em Python é:

```python
from datetime import date

def calculate_room_nights(checkin: date, checkout: date, rooms: int) -> int:
    """Calcula noites de quarto: diferença de dias (não inclusiva) vezes quartos."""
    return (checkout - checkin).days * rooms

```

**Comparando com o C#**

* **Objeto de duração:** No C#, subtrair dois `DateTime` gera um `TimeSpan`, exigindo `.Days` no resultado para multiplicar por um inteiro: `(checkout - checkin).Days * rooms`. O Python segue a mesma lógica com `timedelta.days`.
* **Como o Python sabe o tipo:** Diferente do C#, as *type hints* do Python (`checkin: date`) servem apenas para análise estática e IDEs, não sendo validadas na execução. Ainda assim, como o Python tem tipagem dinâmica e forte, em tempo de execução o próprio objeto `date` resolve o operador `-` e devolve o `timedelta` corretamente.

## Interação 2

### Prompt

class CsvReservationRepository:

    def __init__(self, path: Path) -> None:
        self._path = path

// isso é semelhante a um construtor do c#, certo?

### Resposta

Sim, na prática o `__init__` cumpre exatamente o mesmo papel de um construtor no C#: receber parâmetros ou dependências e inicializar o estado do objeto assim que ele é instanciado.

Algumas equivalências e detalhes importantes na transição do C# para o Python:

* **`self` equivale ao `this`:** A diferença é que o Python exige que você o declare explicitamente como o primeiro parâmetro de todo método de instância. Na hora de instanciar (`repo = CsvReservationRepository(caminho)`), o Python injeta o `self` automaticamente.
* **Inicializador vs. Construtor:** Tecnicamente, o Python divide a construção em duas etapas: o método `__new__` aloca o objeto na memória e o `__init__` o inicializa (por isso ele recebe `self` já criado e retorna `None`). No dia a dia, porém, é no `__init__` que vai toda a lógica que você colocaria em um construtor C#.
* **Encapsulamento (`self._path`):** O Python não possui palavras-chave como `private` ou `readonly`. O *underline* simples no início do nome (`_path`) é a convenção oficial da linguagem para sinalizar que aquele atributo é interno/privado e não deve ser acessado de fora da classe.
* **Sem sobrecarga (*overloading*):** Diferente do C#, você não pode criar múltiplos `__init__` com assinaturas diferentes na mesma classe (o segundo sobrescreveria o primeiro). Para ter múltiplas formas de construir um objeto, usam-se parâmetros com valores padrão ou métodos alternativos decorados com `@classmethod`.

Se a classe existir apenas para armazenar dados sem lógica extra na inicialização, você também pode usar o decorador `@dataclass`, que gera o `__init__` automaticamente de forma parecida com os *Primary Constructors* ou `record` do C#:

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass
class CsvReservationRepository:
    path: Path

```

## Interação 3

### Prompt

{
  "report_version": "1.0",
  "generated_at": "2026-11-14T11:48:12-03:00",
  "summary": {
    "total_reservations": 300,
    "confirmed_reservations": 235,
    "cancelled_reservations": 31,
    "no_show_reservations": 34,
    "total_room_nights": 1347,
    "total_amount_brl": "396170.00",
    "average_nightly_rate_brl": "294.11"
  },
  "by_month": [
    {
      "month": "2024-12",
      "reservations": 35,
      "room_nights": 174,
      "total_brl": "61335.80"
    },
    {
      "month": "2025-01",
      "reservations": 37,
      "room_nights": 235,
      "total_brl": "64662.89"
    },
    {
      "month": "2025-02",
      "reservations": 26,
      "room_nights": 138,
      "total_brl": "45991.09"
    },
    {
      "month": "2025-03",
      "reservations": 39,
      "room_nights": 215,
      "total_brl": "65984.99"
    },
    {
      "month": "2025-04",
      "reservations": 21,
      "room_nights": 146,
      "total_brl": "31335.97"
    },
    {
      "month": "2025-05",
      "reservations": 39,
      "room_nights": 196,
      "total_brl": "63507.98"
    },
    {
      "month": "2025-06",
      "reservations": 38,
      "room_nights": 243,
      "total_brl": "63351.29"
    }
  ],
  "top_hotels": [
    {
      "hotel_id": "H06",
      "hotel_name": "Hotel Salvador Centro",
      "room_nights": 160,
      "total_brl": "45165.46"
    },
    {
      "hotel_id": "H10",
      "hotel_name": "Hotel Madrid, Gran Vía",
      "room_nights": 120,
      "total_brl": "45041.69"
    },
    {
      "hotel_id": "H12",
      "hotel_name": "Hotel Miami Beach",
      "room_nights": 106,
      "total_brl": "41647.69"
    },
    {
      "hotel_id": "H07",
      "hotel_name": "Hotel Brasília Tower",
      "room_nights": 148,
      "total_brl": "39920.52"
    },
    {
      "hotel_id": "H11",
      "hotel_name": "Hotel Buenos Aires",
      "room_nights": 102,
      "total_brl": "37455.69"
    }
  ]
}

// some as reservas e o valor, faça a média e veja se bate com o total

### Resposta

```python
import json
from decimal import Decimal, ROUND_HALF_UP

data = {
  "summary": {
    "total_reservations": 300,
    "confirmed_reservations": 235,
    "cancelled_reservations": 31,
    "no_show_reservations": 34,
    "total_room_nights": 1347,
    "total_amount_brl": "396170.00",
    "average_nightly_rate_brl": "294.11"
  },
  "by_month": [
    {"month": "2024-12", "reservations": 35, "room_nights": 174, "total_brl": "61335.80"},
    {"month": "2025-01", "reservations": 37, "room_nights": 235, "total_brl": "64662.89"},
    {"month": "2025-02", "reservations": 26, "room_nights": 138, "total_brl": "45991.09"},
    {"month": "2025-03", "reservations": 39, "room_nights": 215, "total_brl": "65984.99"},
    {"month": "2025-04", "reservations": 21, "room_nights": 146, "total_brl": "31335.97"},
    {"month": "2025-05", "reservations": 39, "room_nights": 196, "total_brl": "63507.98"},
    {"month": "2025-06", "reservations": 38, "room_nights": 243, "total_brl": "63351.29"}
  ]
}

sum_res_month = sum(m["reservations"] for m in data["by_month"])
sum_nights_month = sum(m["room_nights"] for m in data["by_month"])
sum_brl_month = sum(Decimal(m["total_brl"]) for m in data["by_month"])

sum_status = (
    data["summary"]["confirmed_reservations"] +
    data["summary"]["cancelled_reservations"] +
    data["summary"]["no_show_reservations"]
)

avg_rate_from_summary = Decimal(data["summary"]["total_amount_brl"]) / Decimal(data["summary"]["total_room_nights"])
avg_rate_from_months = sum_brl_month / Decimal(sum_nights_month)
avg_ticket_res = sum_brl_month / Decimal(sum_res_month)

print(f"Soma reservas by_month: {sum_res_month}")
print(f"Soma status (conf+canc+noshow): {sum_status}")
print(f"Soma room_nights by_month: {sum_nights_month}")
print(f"Soma total_brl by_month: {sum_brl_month}")
print(f"Diferença total_brl: {sum_brl_month - Decimal(data['summary']['total_amount_brl'])}")
print(f"Média diária (summary): {avg_rate_from_summary:.6f} -> {avg_rate_from_summary.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
print(f"Média diária (by_month): {avg_rate_from_months:.6f} -> {avg_rate_from_months.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")
print(f"Ticket médio por reserva (235): {avg_ticket_res:.6f} -> {avg_ticket_res.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}")


```

```text
Soma reservas by_month: 235
Soma status (conf+canc+noshow): 300
Soma room_nights by_month: 1347
Soma total_brl by_month: 396170.01
Diferença total_brl: 0.01
Média diária (summary): 294.112843 -> 294.11
Média diária (by_month): 294.112851 -> 294.11
Ticket médio por reserva (235): 1685.829830 -> 1685.83


```

Abaixo está a conferência passo a passo somando os valores discriminados em `by_month` e comparando com o bloco `summary`:

**1. Soma das Reservas**

* **Por mês (`by_month`):** $35 + 37 + 26 + 39 + 21 + 39 + 38 = \mathbf{235}$
* **Por status (`summary`):** $235 \text{ (confirmadas)} + 31 \text{ (canceladas)} + 34 \text{ (no-show)} = \mathbf{300}$
* *Observação:* O agrupamento mensal considera apenas as reservas **confirmadas** (`235`), e não o total geral de reservas registradas (`300`).

**2. Soma das Noites de Quarto (`room_nights`)**

* **Por mês:** $174 + 235 + 138 + 215 + 146 + 196 + 243 = \mathbf{1.347}$
* **No `summary`:** $\mathbf{1.347}$

**3. Soma dos Valores (`total_brl`)**

* **Por mês:**

$$61.335,80 + 64.662,89 + 45.991,09 + 65.984,99 + 31.335,97 + 63.507,98 + 63.351,29 = \mathbf{396.170,01}$$


* **No `summary` (`total_amount_brl`):** $\mathbf{396.170,00}$

**4. Cálculo das Médias**

* **Diária média (`total_amount_brl / total_room_nights`):**

$$\frac{396.170,00}{1.347} = 294,1128... \approx \mathbf{294,11}$$



*(Mesmo usando `396.170,01`, o resultado arredondado continua **294,11**.)*
* **Ticket médio por reserva confirmada (`total_amount_brl / confirmed_reservations`):**

$$\frac{396.170,00}{235} = 1.685,8297... \approx \mathbf{1.685,83}$$



Os números **batem**, com uma diferença de apenas **R$ 0,01** na soma dos valores mensais (`396.170,01` contra `396.170,00` no resumo). Essa divergência de 1 centavo é um comportamento esperado quando cada mês em `by_month` é arredondado para duas casas decimais separadamente antes da soma, enquanto o `total_amount_brl` do `summary` soma os valores brutos exatos e arredonda apenas no final.

## Interação 4

### Prompt

existe alguma forma de rodar o pytest de maneira mais detalhada do que o -q?

### Resposta

O oposto do `-q` (*quiet*) é a família de flags `-v` (*verbose*), que pode ser combinada com outras opções para inspecionar variáveis, `print()` e diferenças completas em estruturas de dados:

| Comando | O que faz |
| --- | --- |
| `pytest` (sem flags) | Padrão da ferramenta. Mostra os arquivos, a porcentagem de progresso e o *traceback* das falhas. |
| `pytest -v` | Lista cada teste individualmente (`arquivo.py::test_nome`) com o status explícito (`PASSED`, `FAILED`, `SKIPPED`). |
| `pytest -vv` | **Verbosidade máxima.** Além de listar os testes, evita que o pytest corte (`...`) diferenças longas em `assert` de dicionários, listas ou JSONs. |
| `pytest -s` | Desativa a captura de *stdout*, permitindo que `print()` e logs apareçam no terminal em tempo real. |
| `pytest -l` | Em caso de falha, imprime o valor de todas as variáveis locais de cada frame do *traceback*. |
| `pytest --tb=long` | Exibe o *traceback* mais detalhado possível na falha (outras opções são `short`, `line` e `no`). |
| `pytest -rA` | Mostra um bloco de resumo ao final listando **todos** os testes (incluindo os que passaram), e não apenas os que falharam. |

**Combinação mais usada para depurar falhas:**

```bash
pytest -vv -s -l

```

Se quiser que o `-v` seja o comportamento padrão do seu projeto sem precisar digitá-lo toda vez, basta configurar no seu `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "-v"

```

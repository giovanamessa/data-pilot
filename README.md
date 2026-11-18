# 📊 Data Pilot

Projeto desenvolvido como parte de um desafio da **DIO (Digital Innovation One)**.

O **Data Pilot** é uma aplicação de análise de vendas desenvolvida em Python que combina um painel interativo com um assistente de IA.

A aplicação permite visualizar indicadores de vendas e fazer perguntas em linguagem natural sobre os dados.

O princípio central do projeto é:

> **O Python calcula. A IA explica.**

Dessa forma, os cálculos das métricas são realizados diretamente sobre os dados pela aplicação, enquanto o modelo de IA interpreta a pergunta, seleciona a ferramenta adequada e apresenta o resultado ao usuário.

---

## 🚀 Funcionalidades

O projeto possui dois módulos principais:

### 📊 Painel de vendas

O painel foi desenvolvido com **Streamlit** e utiliza **Plotly** para visualização dos dados.

Principais informações apresentadas:

- Receita total dos pedidos concluídos
- Quantidade de pedidos concluídos
- Ticket médio
- Receita mensal
- Filtro por categoria
- Top 5 cidades por receita

Com todos os dados selecionados, foram obtidos:

- **Receita total:** R$ 653.416,96
- **Pedidos concluídos:** 295
- **Ticket médio:** R$ 2.214,97

---

## 💬 Conversar com os dados

O Data Pilot possui também uma interface de chat integrada ao **OpenRouter**.

O usuário pode realizar perguntas em português, como:

> Qual é a receita total dos pedidos concluídos?

O modelo identifica a intenção da pergunta e escolhe a função Python adequada.

Exemplo:

`pergunta → calcular_receita → Python calcula → IA explica`

Para a pergunta sobre receita total, o cálculo realizado pelo Python retorna:

**R$ 653.416,96**

A IA recebe esse resultado e o apresenta ao usuário em linguagem natural.

---

## 🛠️ Ferramentas disponíveis para a IA

O modelo pode escolher entre as seguintes funções:

### `calcular_receita`

Calcula a receita total considerando somente os pedidos concluídos.

### `calcular_pedidos`

Retorna a quantidade de pedidos concluídos.

### `calcular_ticket_medio`

Calcula o ticket médio considerando somente os pedidos concluídos.

### `calcular_clientes_unicos`

Retorna a quantidade de clientes únicos entre os pedidos concluídos.

### `calcular_taxa_cancelamento`

Calcula o percentual de pedidos cancelados em relação ao total de pedidos.

---

## 🧹 Tratamento dos dados

A base utilizada pelo projeto está disponível em:

`data/sales.csv`

O tratamento foi realizado com **pandas** e inclui:

1. Leitura do arquivo CSV
2. Conversão da coluna de data
3. Padronização dos valores de status
4. Remoção de registros duplicados
5. Criação da coluna `receita`

A receita de cada registro é calculada por:

`receita = quantidade × preco_unitario`

Durante a análise, os diferentes formatos existentes na coluna de status foram padronizados para:

- `concluido`
- `cancelado`

Após a limpeza, a base permaneceu com **500 registros**, sendo:

- **295 pedidos concluídos**
- **205 pedidos cancelados**

---

## 🏆 Melhoria implementada

Além dos requisitos básicos do desafio, foi implementada a análise:

### Top 5 cidades por receita

O gráfico considera somente os pedidos concluídos e apresenta as cinco cidades com maior receita:

| Posição | Cidade | Receita |
|---|---|---:|
| 1 | Porto Alegre | R$ 74.048,64 |
| 2 | Salvador | R$ 67.157,95 |
| 3 | Brasília | R$ 62.762,63 |
| 4 | Rio de Janeiro | R$ 60.964,74 |
| 5 | Fortaleza | R$ 60.066,19 |

O gráfico também acompanha o filtro de categoria disponível no painel.

---

## 📁 Estrutura do projeto

```text
data-pilot/
├── data/
│   └── sales.csv
├── .env.example
├── .gitignore
├── app.py
├── data_pilot.ipynb
├── requirements.txt
└── README.md

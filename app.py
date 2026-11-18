
import json
import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================
# CONFIGURAÇÃO
# =========================

st.set_page_config(
    page_title="Data Pilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Pilot")
st.caption("Painel inteligente de análise de vendas")

# =========================
# DADOS
# =========================

URL_DADOS = "https://raw.githubusercontent.com/giovanamessa/data-pilot/main/data/sales.csv"

df = pd.read_csv(URL_DADOS)

df["data"] = pd.to_datetime(df["data"])
df["status"] = df["status"].str.strip().str.lower()
df = df.drop_duplicates()
df["receita"] = (
    df["quantidade"] * df["preco_unitario"]
).round(2)

# =========================
# FUNÇÕES DE NEGÓCIO
# =========================

def pedidos_concluidos(dados):
    return dados[dados["status"] == "concluido"]


def calcular_receita(dados):
    concluidos = pedidos_concluidos(dados)
    return round(concluidos["receita"].sum(), 2)


def calcular_pedidos(dados):
    concluidos = pedidos_concluidos(dados)
    return len(concluidos)


def calcular_ticket_medio(dados):
    concluidos = pedidos_concluidos(dados)

    if len(concluidos) == 0:
        return 0

    return round(
        concluidos["receita"].sum() / len(concluidos),
        2
    )


def calcular_clientes_unicos(dados):
    concluidos = pedidos_concluidos(dados)
    return concluidos["cliente_id"].nunique()


def calcular_taxa_cancelamento(dados):
    if len(dados) == 0:
        return 0

    cancelados = len(
        dados[dados["status"] == "cancelado"]
    )

    return round(
        (cancelados / len(dados)) * 100,
        2
    )


# =========================
# FERRAMENTAS DA IA
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calcular_receita",
            "description": "Calcula a receita total dos pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_pedidos",
            "description": "Calcula a quantidade total de pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_ticket_medio",
            "description": "Calcula o ticket médio dos pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_clientes_unicos",
            "description": "Calcula a quantidade de clientes únicos nos pedidos concluídos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calcular_taxa_cancelamento",
            "description": "Calcula a porcentagem de pedidos cancelados em relação ao total de pedidos.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

funcoes_disponiveis = {
    "calcular_receita": calcular_receita,
    "calcular_pedidos": calcular_pedidos,
    "calcular_ticket_medio": calcular_ticket_medio,
    "calcular_clientes_unicos": calcular_clientes_unicos,
    "calcular_taxa_cancelamento": calcular_taxa_cancelamento
}

# =========================
# MENU
# =========================

menu = st.sidebar.radio(
    "Menu",
    ["📊 Painel", "💬 Conversar com os dados"]
)

# =========================
# PAINEL
# =========================

if menu == "📊 Painel":

    st.sidebar.header("Filtros")

    categorias = (
        ["Todas"] +
        sorted(df["categoria"].unique().tolist())
    )

    categoria = st.sidebar.selectbox(
        "Categoria",
        categorias
    )

    if categoria == "Todas":
        dados_filtrados = df.copy()
    else:
        dados_filtrados = df[
            df["categoria"] == categoria
        ].copy()

    concluidos = pedidos_concluidos(dados_filtrados)

    receita_total = calcular_receita(dados_filtrados)
    total_pedidos = calcular_pedidos(dados_filtrados)
    ticket_medio = calcular_ticket_medio(dados_filtrados)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Receita total",
        f"R$ {receita_total:,.2f}"
    )

    col2.metric(
        "📦 Pedidos concluídos",
        total_pedidos
    )

    col3.metric(
        "🧾 Ticket médio",
        f"R$ {ticket_medio:,.2f}"
    )

    st.divider()

    receita_mensal = (
        concluidos
        .assign(
            mes=concluidos["data"]
            .dt.to_period("M")
            .astype(str)
        )
        .groupby("mes", as_index=False)["receita"]
        .sum()
    )

    fig = px.line(
        receita_mensal,
        x="mes",
        y="receita",
        markers=True,
        title="Receita por mês"
    )

    fig.update_layout(
        xaxis_title="Mês",
        yaxis_title="Receita (R$)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # =========================
    # MELHORIA: TOP 5 CIDADES
    # =========================

    st.divider()

    top_cidades = (
        concluidos
        .groupby("cidade", as_index=False)["receita"]
        .sum()
        .sort_values("receita", ascending=False)
        .head(5)
    )

    fig_cidades = px.bar(
        top_cidades,
        x="cidade",
        y="receita",
        text_auto=".2s",
        title="Top 5 cidades por receita"
    )

    fig_cidades.update_layout(
        xaxis_title="Cidade",
        yaxis_title="Receita (R$)"
    )

    st.plotly_chart(
        fig_cidades,
        use_container_width=True
    )

# =========================
# CHAT
# =========================

else:

    st.header("💬 Conversar com os dados")

    st.caption(
        "Pergunte sobre receita, pedidos, ticket médio, "
        "clientes únicos ou taxa de cancelamento."
    )

    pergunta = st.chat_input(
        "Ex.: Qual é a receita total?"
    )

    if pergunta:

        st.chat_message("user").write(pergunta)

        # No Colab, usaremos variável de ambiente.
        # No projeto final, esta chave virá do .env.
        api_key = os.getenv("OPENROUTER_API_KEY")

        if not api_key:
            st.error(
                "OPENROUTER_API_KEY não configurada "
                "no ambiente da aplicação."
            )
            st.stop()

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        messages = [
            {
                "role": "system",
                "content": (
                    "Você é o assistente do Data Pilot. "
                    "Para perguntas sobre métricas de vendas, "
                    "use sempre as ferramentas disponíveis. "
                    "O Python calcula os números. "
                    "Você apenas explica o resultado. "
                    "Nunca invente ou recalcule valores."
                )
            },
            {
                "role": "user",
                "content": pergunta
            }
        ]

        payload = {
            "model": "openrouter/free",
            "messages": messages,
            "tools": tools,
            "tool_choice": "auto"
        }

        try:

            resposta = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )

            resposta.raise_for_status()

            mensagem = resposta.json()[
                "choices"
            ][0]["message"]

            if mensagem.get("tool_calls"):

                tool_call = mensagem["tool_calls"][0]

                nome_ferramenta = (
                    tool_call["function"]["name"]
                )

                if nome_ferramenta not in funcoes_disponiveis:
                    st.error(
                        "A IA solicitou uma ferramenta "
                        "não disponível."
                    )
                    st.stop()

                funcao = funcoes_disponiveis[
                    nome_ferramenta
                ]

                resultado_python = funcao(df)

                messages.append(mensagem)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": str(resultado_python)
                    }
                )

                payload_final = {
                    "model": "openrouter/free",
                    "messages": messages,
                    "tools": tools
                }

                resposta_final = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload_final,
                    timeout=60
                )

                resposta_final.raise_for_status()

                texto_final = (
                    resposta_final.json()
                    ["choices"][0]["message"]["content"]
                )

                st.chat_message(
                    "assistant"
                ).write(texto_final)

                with st.expander(
                    "🔧 Ferramenta utilizada"
                ):
                    st.write(nome_ferramenta)
                    st.write(
                        "Resultado calculado pelo Python:",
                        resultado_python
                    )

            else:

                st.chat_message(
                    "assistant"
                ).write(
                    mensagem.get(
                        "content",
                        "Não consegui responder."
                    )
                )

        except requests.RequestException as erro:

            st.error(
                f"Erro ao acessar o OpenRouter: {erro}"
            )

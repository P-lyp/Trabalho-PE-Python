import streamlit as st
import requests

st.title("Conversor de Projetos Freelancer") 
# campos que o usuário preenche/escolhe
nome_projeto = st.text_input(label="Nome do Projeto") 
valor = st.number_input("Digite o valor", min_value=0.0, value=1.0) 
tipo_moeda = st.radio("Tipo da moeda", ["Tradicional", "Cripto"]) 

# array com as opções de moedas
lista_moeda_trad = ["USD","EUR","JPY","GBP","AUD","CAD","CHF","CNY","HKD","NZD","SEK","NOK","SGD","KRW","INR","BRL","MXN","ZAR","RUB","TRY"]
lista_moeda_cripto = ["BTC","ETH","BNB","USDT","SOL","XRP","USDC","ADA","DOGE","TON","AVAX","DOT","TRX","SHIB","WBTC","LINK","LTC","MATIC","BCH","XLM"]

# Condicional que verifica o tipo selecionado para exibir a lista de opções de moedas
if tipo_moeda == "Tradicional" :
    moeda_origem = st.selectbox("Moeda de Origem", lista_moeda_trad)

else:
    moeda_origem = st.selectbox("Moeda de Origem", lista_moeda_cripto)

# Dados para comunicação com api
api_key_trad = "30a78cc1afa0ed31153a6960"
api_url_trad = f"https://v6.exchangerate-api.com/v6/{api_key_trad}/pair/{moeda_origem}/BRL/{valor}"
api_url_cripto = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=brl&symbols={moeda_origem}"

# se ainda não existir a variável total_recebido na memória da sessão, cria ela - o st.session_state é utilizado para manter os dados entre as interações na página, sendo uma espeécie de memória
if "total_recebido" not in st.session_state: 
    st.session_state.total_recebido = 0.0 

if "historico_conversoes" not in st.session_state:
    st.session_state.historico_conversoes = [] # mesma coisa, se ainda não existir, cria uma lista vazia

# cria o botão de Converter e informa o que será feito ao clicar
if st.button("Converter"):

    # Faz uma verificação do tipo escolhido 
    if tipo_moeda == "Tradicional":
        response = requests.get(api_url_trad) # conecta com a api

        # se o retorno der certo, armazena a informação
        if response.status_code == 200: 
            data = response.json()
            valor_recebido = data["conversion_result"]

            # agrupa os dados da conversão de valores
            info_conversao = f"{nome_projeto} - {valor} {moeda_origem} = R$ {valor_recebido:.2f}"

            # armazena a conversão feita no histórico total
            st.session_state.historico_conversoes.append(info_conversao)
            # soma o valor recebido com a variável que controla o total
            st.session_state.total_recebido += valor_recebido

        else:
            st.error("Erro ao converter. Verifique a chave da API ou as moedas selecionadas.")
   
   # mesmo processo do if anterior
    if tipo_moeda == "Cripto":
        response = requests.get(api_url_cripto)

        if response.status_code == 200:
            data = response.json()
            valor_recebido = data[moeda_origem.lower()]["brl"] * valor

            valor_formatado = f"{valor_recebido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            info_conversao = f"{nome_projeto} - {valor} {moeda_origem} = R$ {valor_formatado}"

            st.session_state.historico_conversoes.append(info_conversao)
            st.session_state.total_recebido += valor_recebido

# cria a sessão para exibir o histórico        
st.subheader("Histórico")        

# se tiver alguma informação no histórico, exibe o valor total recebido e as conversões realizadas
if st.session_state.historico_conversoes:
    valor_formatado = f"{st.session_state.total_recebido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.success(f"Total recebido: R${valor_formatado}")

    for item in st.session_state.historico_conversoes:
        st.write("-", item)
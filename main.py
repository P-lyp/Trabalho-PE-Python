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

api_key_trad = "30a78cc1afa0ed31153a6960"
api_url_trad = f"https://v6.exchangerate-api.com/v6/{api_key_trad}/pair/{moeda_origem}/BRL/{valor}"
api_url_cripto = f"https://api.coingecko.com/api/v3/simple/price?vs_currencies=brl&symbols={moeda_origem}"

# o streamlit fornece o st.session_state para que os dados sejam mantidos entre as interações com a página, como uma espécie de memória 
if "total_recebido" not in st.session_state: 
    st.session_state.total_recebido = 0.0 # se ainda não existir a variável total_recebido na memória da sessão, cria ela com valor inicial 0.0.

if "historico" not in st.session_state:
    st.session_state.historico = [] # mesma coisa, se ainda não existir, cria uma lista vazia

if st.button("Converter"):

    if tipo_moeda == "Tradicional":
        response = requests.get(api_url_trad)

        if response.status_code == 200:
            data = response.json()
            valor_convertido = data["conversion_result"]

            conversao = f"{nome_projeto} - {valor} {moeda_origem} = R$ {valor_convertido:.2f}"

            st.session_state.historico.append(conversao)
            st.session_state.total_recebido += valor_convertido

        
        else:
            st.error("Erro ao converter. Verifique a chave da API ou as moedas selecionadas.")
    
    if tipo_moeda == "Cripto":

        response = requests.get(api_url_cripto)

        if response.status_code == 200:

            data = response.json()

            valor_convertido = data[moeda_origem.lower()]["brl"] * valor

            valor_formatado = f"{valor_convertido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            conversao = f"{nome_projeto} - {valor} {moeda_origem} = R$ {valor_formatado}"

            st.session_state.historico.append(conversao)
            st.session_state.total_recebido += valor_convertido

        
st.subheader("Histórico")        

if st.session_state.historico:

    valor_formatado = f"{st.session_state.total_recebido:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    st.success(f"Total recebido: R${valor_formatado}")

    for item in st.session_state.historico:
        st.write("-", item)
import streamlit as st
import requests

# Função simulada para gerar uma resposta baseada no prompt - substitua com a chamada real à API de IA generativa
def gerar_resposta(prompt):
    return f"Inteli Academy melhor Liga do Inteli"


st.title("Desafios de IA Generativa")

st.write("Digite um prompt e veja a mágica da IA:")

user_input = st.text_input("Prompt:", "")

if st.button("Gerar"):
    if user_input.strip() != "":
        resposta = gerar_resposta(user_input)
        st.write(resposta)
    else:
        st.warning("Digite um prompt antes de gerar!")



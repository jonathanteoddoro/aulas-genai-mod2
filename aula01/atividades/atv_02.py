import streamlit as st

st.set_page_config(page_title="Desafios de IA - Tradutor")

st.title("Desafios de IA Generativa - Tradutor")

st.write("Digite um texto em qualquer idioma e veja a tradução aparecer:")

user_input = st.text_area("Texto a traduzir:", "", height=150)

idioma_alvo = st.selectbox(
    "Escolha o idioma para tradução:",
    ("Português", "Inglês", "Espanhol", "Francês", "Alemão")
)

def traduzir_texto(texto, idioma_destino):
    return "Aqui vai a tradução gerada pela IA (implemente!!!)"

if st.button("Traduzir"):
    if user_input.strip() != "":
        with st.spinner("Traduzindo..."):
            try:
                resultado = traduzir_texto(user_input, idioma_alvo)
                st.markdown(
                    f"""
                    <div style="
                        padding: 15px;
                        border-radius: 10px;
                        margin-top: 10px;
                        font-size: 16px;
                        line-height: 1.5;
                    ">
                        {resultado}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.error(f"Erro ao traduzir: {e}")
    else:
        st.warning("Digite algum texto para traduzir!")

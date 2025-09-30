import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
import json

# PASSO 1: Configure sua chave da OpenAI aqui
OPENAI_API_KEY = "SUA_CHAVE_AQUI"

# PASSO 2: Crie as ferramentas (tools) usando o decorator @tool

@tool
def obter_clima(cidade: str) -> str:
    """
    Retorna informações simuladas sobre o clima de uma cidade.
    
    Args:
        cidade: Nome da cidade para consultar o clima
        
    Returns:
        String com informações do clima
    """
    # TODO: Implemente a lógica da função
    # Dica: Use um dicionário com cidades e suas informações de clima simuladas
    # Exemplo de estrutura:
    # climas = {
    #     "são paulo": {"temp": 25, "condicao": "Ensolarado"},
    #     "rio de janeiro": {"temp": 30, "condicao": "Parcialmente nublado"},
    #     ...
    # }
    # Retorne uma string formatada com as informações
    
    return "IMPLEMENTE AQUI - retorne informações de clima simuladas"


@tool
def converter_moeda(valor: float, moeda_origem: str, moeda_destino: str) -> str:
    """
    Converte valores entre diferentes moedas usando taxas fixas simuladas.
    
    Args:
        valor: Valor a ser convertido
        moeda_origem: Moeda de origem (ex: "BRL", "USD", "EUR")
        moeda_destino: Moeda de destino (ex: "BRL", "USD", "EUR")
        
    Returns:
        String com o resultado da conversão
    """
    # TODO: Implemente a lógica da conversão
    # Dica: Crie um dicionário com taxas de câmbio fixas
    # Exemplo:
    # taxas = {
    #     "BRL": 1.0,
    #     "USD": 5.0,
    #     "EUR": 5.5,
    #     "GBP": 6.3
    # }
    # Converta primeiro para BRL, depois para moeda_destino
    
    return "IMPLEMENTE AQUI - retorne o valor convertido"


@tool
def calcular_imc(peso: float, altura: float) -> str:
    """
    Calcula o Índice de Massa Corporal (IMC) e retorna a classificação.
    
    Args:
        peso: Peso em quilogramas
        altura: Altura em metros
        
    Returns:
        String com o IMC calculado e sua classificação
    """
    # TODO: Implemente o cálculo do IMC
    # Fórmula: IMC = peso / (altura ** 2)
    # Classificações:
    # < 18.5: Abaixo do peso
    # 18.5-24.9: Peso normal
    # 25-29.9: Sobrepeso
    # >= 30: Obesidade
    
    return "IMPLEMENTE AQUI - retorne o IMC e classificação"


# =============================================================================
# PASSO 3: Configure o agente com as ferramentas
# =============================================================================

def criar_agente():
    """
    Cria e configura o agente com as ferramentas disponíveis.
    """
    # TODO: Complete a configuração do agente
    
    # 3.1: Inicialize o modelo da OpenAI
    llm = ChatOpenAI(
        model="gpt-4o-mini",  
        api_key=OPENAI_API_KEY,
        temperature=0.3
    )
    
    # 3.2: Liste suas ferramentas criadas
    tools = [
    ]
    
    # 3.3: Crie o prompt do agente
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente útil que pode ajudar com:
        - Informações de clima de cidades
        - Conversão de moedas
        - Cálculo de IMC
        
        Seja amigável e forneça respostas claras e objetivas."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # 3.4: Crie o agente e o executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,  
        handle_parsing_errors=True
    )
    
    return agent_executor


# INTERFACE STREAMLIT

st.set_page_config(page_title="Function Calling com LangChain", page_icon="🤖")
st.title("Assistente Multi-funções")
st.write("Este assistente pode ajudar você com clima, conversões de moeda e cálculo de IMC!")

with st.expander("Exemplos de perguntas"):
    st.markdown("""
    **Clima:**
    - "Como está o clima em São Paulo?"
    - "Qual a temperatura no Rio de Janeiro?"
    
    **Conversão de Moedas:**
    - "Converta 100 dólares para reais"
    - "Quanto é 50 euros em libras?"
    
    **Cálculo de IMC:**
    - "Calcule meu IMC, peso 70kg e altura 1.75m"
    - "Qual meu IMC se peso 85kg e tenho 1.80m?"
    
    **Perguntas combinadas:**
    - "Qual o clima em Paris e quanto custa 200 euros em reais?"
    """)

# Input do usuário
user_query = st.text_area(
    "Faça sua pergunta:",
    placeholder="Ex: Como está o clima em São Paulo?",
    height=100
)

if st.button("🚀 Enviar", type="primary"):
    if user_query.strip():
        with st.spinner("Processando sua solicitação..."):
            try:
                # TODO: Execute o agente aqui
                # Dica: Use agent_executor.invoke({"input": user_query})
                
                agent_executor = criar_agente()
                resposta = agent_executor.invoke({"input": user_query})
                
                st.success("Resposta:")
                st.markdown(f"""
                <div style="
                    background-color: #f0f2f6;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 5px solid #4CAF50;
                    margin-top: 10px;
                ">
                    {resposta['output']}
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("Ver detalhes da execução"):
                    st.json(resposta)
                    
            except Exception as e:
                st.error(f"Erro ao processar: {str(e)}")
                st.info("Verifique se você configurou a API key corretamente!")
    else:
        st.warning("Por favor, digite uma pergunta!")

# Sidebar com informações
with st.sidebar:
    st.header("Sobre este projeto")
    st.markdown("""
    Este é um exercício de **Function Calling** usando LangChain.
    
    **Tecnologias:**
    - LangChain
    - OpenAI API
    - Streamlit
    
    **Objetivos de aprendizado:**
    1. Criar ferramentas personalizadas com `@tool`
    2. Configurar agentes com function calling
    3. Integrar múltiplas ferramentas
    4. Processar linguagem natural
    """)
    
    st.divider()
    
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# CONFIGURAÇÃO DA API
OPENAI_API_KEY = "SUA_CHAVE_AQUI"

@tool
def calcular_soma(numero1: float, numero2: float) -> str:
    """
    Calcula a soma de dois números.
    
    Args:
        numero1: Primeiro número
        numero2: Segundo número
        
    Returns:
        String com o resultado da soma
    """
    resultado = numero1 + numero2
    return f"A soma de {numero1} + {numero2} = {resultado}"


@tool
def calcular_produto(numero1: float, numero2: float) -> str:
    """
    Calcula o produto (multiplicação) de dois números.
    
    Args:
        numero1: Primeiro número
        numero2: Segundo número
        
    Returns:
        String com o resultado da multiplicação
    """
    resultado = numero1 * numero2
    return f"O produto de {numero1} × {numero2} = {resultado}"


@tool
def verificar_par_impar(numero: int) -> str:
    """
    Verifica se um número é par ou ímpar.
    
    Args:
        numero: Número inteiro para verificar
        
    Returns:
        String indicando se o número é par ou ímpar
    """
    if numero % 2 == 0:
        return f"O número {numero} é PAR"
    else:
        return f"O número {numero} é ÍMPAR"


# CONFIGURAÇÃO DO AGENTE

def criar_agente():
    """Cria e configura o agente com as ferramentas."""
    
    # Inicializar o modelo
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=OPENAI_API_KEY,
        temperature=0
    )
    
    # Lista de ferramentas
    tools = [
        calcular_soma,
        calcular_produto,
        verificar_par_impar
    ]
    
    # Prompt do agente
    prompt = ChatPromptTemplate.from_messages([
        ("system", """Você é um assistente matemático amigável.
        Você pode:
        - Somar dois números
        - Multiplicar dois números
        - Verificar se um número é par ou ímpar
        
        Seja claro e educado nas respostas."""),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Criar agente e executor
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor


# INTERFACE STREAMLIT

st.set_page_config(
    page_title="Demo Function Calling",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Assistente Matemático")
st.write("Demonstração de Function Calling com LangChain")

# Sidebar com informações
with st.sidebar:
    st.header("📚 Como funciona?")
    st.markdown("""
    Este assistente usa **Function Calling**:
    
    1. Você faz uma pergunta em linguagem natural
    2. A IA **entende sua intenção**
    3. A IA **escolhe a ferramenta certa**
    4. A ferramenta é executada automaticamente
    5. Você recebe a resposta
    
    **Mágica da IA:** Você não precisa dizer qual função usar!
    """)
    
    st.divider()
    
    st.header("🛠️ Ferramentas disponíveis")
    st.markdown("""
    - Calcular soma
    - Calcular produto
    - Verificar par/ímpar
    """)

# Área de exemplos
with st.expander("Exemplos de perguntas", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Soma:**")
        st.code("Quanto é 15 + 23?")
        st.code("Some 100 e 250")
        
        st.markdown("**Multiplicação:**")
        st.code("Multiplique 7 por 8")
        st.code("Quanto é 12 vezes 15?")
    
    with col2:
        st.markdown("**Par ou Ímpar:**")
        st.code("42 é par ou ímpar?")
        st.code("Verifique se 77 é par")
        
        st.markdown("**Combinadas:**")
        st.code("Some 10 e 5, depois verifique se o resultado é par")

# Input do usuário
st.markdown("---")
user_query = st.text_input(
    "Faça sua pergunta:",
    placeholder="Ex: Quanto é 25 + 37?",
    key="query_input"
)

# Botões de exemplo rápido
st.markdown("**Ou clique em um exemplo:**")
col1, col2, col3 = st.columns(3)

if col1.button("Soma", use_container_width=True):
    user_query = "Quanto é 15 + 23?"
    
if col2.button("✖️ Multiplicação", use_container_width=True):
    user_query = "Multiplique 7 por 8"
    
if col3.button("🔢 Par/Ímpar", use_container_width=True):
    user_query = "O número 42 é par ou ímpar?"

# Processar pergunta
if st.button("🚀 Processar", type="primary", use_container_width=True) or user_query:
    if user_query and user_query.strip():
        with st.spinner("🤔 Pensando..."):
            try:
                # Criar e executar agente
                agent_executor = criar_agente()
                resposta = agent_executor.invoke({"input": user_query})
                
                # Mostrar resposta
                st.success("✅ Resposta do Assistente:")
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 25px;
                    border-radius: 15px;
                    font-size: 18px;
                    font-weight: 500;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    margin: 20px 0;
                ">
                    {resposta['output']}
                </div>
                """, unsafe_allow_html=True)
                
                # Mostrar processo (para fins educacionais)
                with st.expander("🔍 Ver processo de decisão da IA"):
                    st.markdown("**Pergunta original:**")
                    st.info(user_query)
                    
                    st.markdown("**Resposta completa do agente:**")
                    st.json(resposta)
                    
                    st.markdown("""
                    **O que aconteceu:**
                    1. A IA leu sua pergunta
                    2. Analisou qual ferramenta usar
                    3. Extraiu os parâmetros necessários
                    4. Executou a ferramenta
                    5. Formatou a resposta
                    """)
                
            except Exception as e:
                st.error(f"Erro ao processar: {str(e)}")
                
                if "api key" in str(e).lower():
                    st.warning("""
                    **Problema com a API Key!**
                    
                    Verifique se você:
                    1. Configurou a chave na linha 10
                    2. A chave é válida e ativa
                    3. Tem créditos disponíveis
                    """)
    else:
        st.warning("Por favor, digite uma pergunta ou clique em um exemplo!")

# Footer com informações técnicas
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <small>
        🔧 Tecnologias: LangChain + OpenAI + Streamlit<br>
        📖 Demonstração de Function Calling para fins educacionais
    </small>
</div>
""", unsafe_allow_html=True)
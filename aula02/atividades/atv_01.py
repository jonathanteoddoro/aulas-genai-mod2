import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from langchain.schema import Document

# Configure sua chave da OpenAI aqui
os.environ["OPENAI_API_KEY"] = "sua_api_key_aqui"

# Dados mockados sobre o Inteli Academy - Liga de IA
documentos_inteli = [
    """
    O Inteli é uma faculdade de tecnologia localizada em São Paulo que se destaca pela formação 
    inovadora em tecnologia e negócios. A instituição oferece cursos de graduação focados em ciência da 
    computação, engenharia de software, sistemas de informação e engenharia da computação. O Inteli adota 
    uma metodologia baseada em projetos reais, onde os estudantes trabalham em parceria com empresas 
    desde o primeiro semestre. A instituição tem parcerias com grandes empresas como Dell, IBM, Oracle e 
    outras multinacionais, proporcionando experiências práticas autênticas aos alunos.
    """,
    """
    O Inteli Academy é uma liga de IA focada exclusivamente em 
    Inteligência Artificial e Machine Learning. Esta liga reúne os estudantes mais talentosos e 
    interessados em IA do Inteli Academy, proporcionando treinamento avançado, projetos de pesquisa e desenvolvimento 
    de soluções inovadoras. Os membros da Liga de IA participam de competições nacionais e 
    internacionais, desenvolvem papers acadêmicos e trabalham em projetos de ponta com tecnologias 
    emergentes como GPT, computer vision, processamento de linguagem natural e redes neurais profundas. 
    A liga também organiza eventos, workshops e palestras com especialistas da indústria.
    """,
    """
    Os projetos desenvolvidos pelos estudantes do Inteli Academy são sempre baseados em problemas 
    reais de empresas parceiras. Na Liga de IA, os projetos incluem sistemas de recomendação, 
    chatbots inteligentes, análise preditiva, visão computacional para automação industrial, 
    processamento de linguagem natural para análise de sentimentos, e desenvolvimento de modelos 
    de machine learning para otimização de processos empresariais. Os alunos trabalham com 
    frameworks modernos como TensorFlow, PyTorch, Scikit-learn e ferramentas de MLOps como MLflow 
    e Kubeflow. Cada projeto tem duração de um semestre e resulta em soluções funcionais que são 
    apresentadas para as empresas parceiras.
    """,
    """
    A metodologia do Inteli Academy é centrada no aprendizado por projetos (PBL - Project Based Learning). 
    Os estudantes trabalham em equipes multidisciplinares para resolver desafios reais apresentados por 
    empresas parceiras. Cada semestre é organizado em torno de um projeto principal, complementado por 
    aulas teóricas e workshops práticos. A Liga de IA, como programa do Inteli Academy, segue essa mesma metodologia, mas com foco 
    específico em desafios de inteligência artificial. Os professores atuam como mentores e facilitadores, 
    guiando os estudantes no processo de descoberta e solução de problemas. Esta abordagem desenvolve 
    não apenas competências técnicas, mas também habilidades de trabalho em equipe, comunicação e 
    pensamento crítico.
    """,
    """
    O Inteli Academy foi fundado com a missão de revolucionar o ensino superior em tecnologia no Brasil. 
    A instituição nasceu da percepção de que o mercado de trabalho demanda profissionais que combinem 
    excelência técnica com visão de negócios e capacidade de inovação. O campus do Inteli Academy é equipado 
    com laboratórios de última geração, incluindo labs de IA, robótica, IoT e realidade virtual. 
    A Liga de IA, como programa especial do Inteli Academy, tem acesso a recursos computacionais avançados, incluindo GPUs para treinamento de 
    modelos de deep learning e plataformas cloud para desenvolvimento e deployment de soluções de IA. 
    A instituição mantém um forte foco na empregabilidade, com taxa de emprego dos formandos próxima 
    a 100% em grandes empresas de tecnologia.
    """
]

# Implementação RAG Simples - Baseada no exemplo da aula02.md
print("🔍 Sistema RAG - Inteli Academy & Liga de IA")
print("=" * 50)

print("📚 Carregando documentos...")

# Divisão em chunks usando CharacterTextSplitter (como no exemplo da aula)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

# Criar documentos a partir dos textos
documents = [Document(page_content=doc) for doc in documentos_inteli]

# Dividir os documentos em chunks (como no exemplo da aula)
texts = text_splitter.split_documents(documents)
print(f"✂️ Criados {len(texts)} fragmentos de texto")

# Criação de embeddings e base vetorial (como no exemplo da aula)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(texts, embeddings)
print("🎯 Base vetorial criada com sucesso!")

# Cliente OpenAI para RAG manual
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

def buscar_resposta_rag(pergunta, vectorstore):
    """Implementação RAG manual usando diretamente a OpenAI"""
    # Recuperar documentos relevantes
    docs = vectorstore.similarity_search(pergunta, k=3)
    
    # Construir contexto a partir dos documentos recuperados
    contexto = "\n\n".join([doc.page_content for doc in docs])
    
    # Criar prompt estruturado
    prompt = f"""Baseado nas informações fornecidas sobre o Inteli Academy, responda à pergunta de forma precisa e detalhada.

    CONTEXTO:
    {contexto}

    PERGUNTA: {pergunta}

    INSTRUÇÕES:
    - Use apenas as informações do contexto fornecido
    - Seja específico e preciso na resposta
    - Se a informação não estiver no contexto, informe que não foi encontrada

    RESPOSTA:"""

    # Chamada para OpenAI Chat Completions
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um assistente especializado em responder perguntas sobre o Inteli Academy baseado apenas nos documentos fornecidos."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content

print("\n✅ Sistema RAG iniciado com sucesso!")

print("\n" + "=" * 50)
print("Digite suas perguntas (ou 'sair' para encerrar):")

# Loop principal para perguntas
while True:
    print("\n" + "-" * 30)
    pergunta = input("🤔 Sua pergunta: ").strip()
    
    if "sair" in pergunta.lower():
        print("👋 Encerrando sistema RAG. Até logo!")
        break

    # Uso do RAG manual com OpenAI direta
    resposta = buscar_resposta_rag(pergunta, vectorstore)
    
    print("\n📝 Resposta:")
    print(f"{resposta}")
        
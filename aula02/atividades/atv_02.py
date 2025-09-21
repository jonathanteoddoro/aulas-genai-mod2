import streamlit as st
import os
import tempfile
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from langchain.schema import Document

def configurar_pagina():
    st.set_page_config(
        page_title="RAG com PDF", 
        page_icon="📄", 
        layout="wide"
    )
    
    st.title("📄 RAG com Processamento de PDF")
    st.markdown("""
    Este sistema permite fazer upload de documentos PDF e realizar consultas inteligentes 
    sobre o conteúdo usando RAG (Retrieval Augmented Generation).
    """)

os.environ["OPENAI_API_KEY"] = "sua_api_key_aqui"

def extrair_texto_pdf(arquivo_pdf):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(arquivo_pdf.getvalue())
            tmp_file_path = tmp_file.name
        
        texto_completo = ""
        with open(tmp_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                texto_completo += page.extract_text() + "\n"
        
        os.unlink(tmp_file_path)
        
        return texto_completo.strip()
    
    except Exception as e:
        st.error(f"Erro ao extrair texto do PDF: {e}")
        return None

def criar_base_vetorial(texto):
    try:
        """Espaço para implementar a criação da base vetorial como exercício
            A função deve retornar o objeto vectorstore e o número de chunks criados
            Pode colocar a lógica da atividade a baixo
        """
        return vectorstore, len(texts)
    
    except Exception as e:
        st.error(f"Erro ao criar base vetorial: {e}")
        return None, 0

def buscar_resposta_rag(pergunta, vectorstore):
    try:
        """Espaço para implementar a busca de resposta RAG como exercício
            A função deve retornar a resposta e os documentos relevantes
            Pode colocar a lógica da atividade a baixo
        """
        return response.choices[0].message.content, docs
    
    except Exception as e:
        st.error(f"Erro na consulta RAG: {e}")
        return None, []

def interface_upload():
    st.header("📤 Upload de Documento PDF")
    
    uploaded_file = st.file_uploader(
        "Escolha um arquivo PDF",
        type="pdf",
        help="Faça upload de um documento PDF para análise"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
        st.info(f"📊 Tamanho: {uploaded_file.size / 1024:.1f} KB")
        return uploaded_file
    
    return None

def interface_processamento(uploaded_file):
    if st.button("🔄 Processar Documento", type="primary", key="processar_pdf"):
        with st.spinner("📖 Extraindo texto do PDF..."):
            texto = extrair_texto_pdf(uploaded_file)
            
            if not texto:
                st.error("❌ Não foi possível extrair texto do PDF")
                return None
            
            st.success(f"✅ Texto extraído com sucesso! ({len(texto)} caracteres)")
            
            with st.expander("👁️ Prévia do texto extraído"):
                st.text_area("Texto", texto[:500] + "..." if len(texto) > 500 else texto, height=200)
        
        with st.spinner("🔄 Criando base vetorial..."):
            vectorstore, num_chunks = criar_base_vetorial(texto)
            
            if vectorstore:
                st.success(f"🎯 Base vetorial criada com sucesso! ({num_chunks} fragmentos)")
                return vectorstore
            else:
                st.error("❌ Erro ao criar base vetorial")
                return None
    
    return None

def interface_consulta(vectorstore):
    st.header("💬 Consultas ao Documento")
    
    pergunta = st.text_area(
        "Digite sua pergunta sobre o documento:",
        placeholder="Ex: Qual é o tema principal do documento?",
        height=100
    )
    
    if st.button("🔍 Consultar", type="primary"):
        if not pergunta.strip():
            st.warning("⚠️ Digite uma pergunta!")
        else:
            with st.spinner("🔍 Buscando informações no documento..."):
                resposta, docs_relevantes = buscar_resposta_rag(pergunta, vectorstore)
            
            if resposta:
                st.markdown("### 📝 Resposta:")
                st.write(resposta)
                
                if docs_relevantes:
                    with st.expander("📚 Trechos do documento consultados"):
                        for i, doc in enumerate(docs_relevantes):
                            st.markdown(f"**Trecho {i+1}:**")
                            st.text_area(f"Conteúdo {i+1}", doc.page_content, height=150, key=f"fonte_{i}")
                            st.markdown("---")



def main():
    configurar_pagina()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file = interface_upload()
        
        if uploaded_file:
            vectorstore = interface_processamento(uploaded_file)
            
            if vectorstore:
                st.session_state.vectorstore = vectorstore
    
    with col2:
        if hasattr(st.session_state, 'vectorstore'):
            interface_consulta(st.session_state.vectorstore)
        else:
            st.info("📤 Faça upload e processe um PDF para começar as consultas")

if __name__ == "__main__":
    main()
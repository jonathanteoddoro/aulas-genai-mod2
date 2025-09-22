# Atividade 02 - Sistema RAG com Streamlit (Template de Exercício)

## 📝 Descrição

O código base fornece a estrutura da interface e deixa as **funções principais RAG como exercício** para o estudante implementar, baseando-se na lógica da **Atividade 1**.

## 🎯 Objetivo do Exercício

**Completar a implementação** das funções RAG principais, transferindo a lógica da Atividade 1 para o contexto web:
- `criar_base_vetorial(texto)` 
- `buscar_resposta_rag(pergunta, vectorstore)`

## 🏗️ Estrutura Fornecida

### ✅ **Já Implementado (Interface Streamlit):**

1. **Configuração da Página**: Layout, título e descrição
2. **Upload de PDF**: Interface para seleção de arquivos
3. **Extração de Texto**: Usando PyPDF2 (função completa)
4. **Interface de Processamento**: Botões, spinners e feedback visual
5. **Interface de Consulta**: Campo de pergunta e exibição de resultados
6. **Layout**: Estrutura em colunas e gerenciamento de estado

### ⚠️ **Para Implementar (Lógica RAG):**

1. **`criar_base_vetorial(texto)`**: 
   - Dividir texto em chunks
   - Criar embeddings 
   - Armazenar no Chroma
   - Retornar vectorstore e contagem

2. **`buscar_resposta_rag(pergunta, vectorstore)`**:
   - Buscar documentos similares
   - Construir contexto
   - Chamar OpenAI Chat
   - Retornar resposta e documentos

## 🏗️ Arquitetura do Sistema

### Componentes Principais

1. **Interface Web**: Streamlit para upload e consultas
2. **Extração de Texto**: PyPDF2 para processar documentos PDF
3. **Processamento**: LangChain para divisão em chunks
4. **Embeddings**: OpenAI para conversão em vetores
5. **Base Vetorial**: Chroma para armazenamento e busca
6. **Geração**: OpenAI Chat para respostas contextualizadas

## 🔧 Dependências

```python
import streamlit as st          # Interface web
import os                       # Variáveis de ambiente
import tempfile                 # Arquivos temporários
from pathlib import Path        # Manipulação de caminhos
import PyPDF2                   # Extração de texto PDF
from langchain.text_splitter import CharacterTextSplitter  # Divisão em chunks
from langchain_openai import OpenAIEmbeddings              # Embeddings
from langchain_community.vectorstores import Chroma        # Base vetorial
from openai import OpenAI                                  # API OpenAI
from langchain.schema import Document                       # Estrutura de documentos
```

## � Instruções do Exercício

### 🎯 O que fazer:

1. **Configure sua chave OpenAI**:
   ```python
   os.environ["OPENAI_API_KEY"] = "sua_chave_real_aqui"
   ```

2. **Implemente `criar_base_vetorial(texto)`**:
   - Use a **mesma lógica da Atividade 1**
   - CharacterTextSplitter com chunk_size=1000, overlap=200
   - OpenAIEmbeddings + Chroma.from_documents
   - Retorne (vectorstore, len(texts))

3. **Implemente `buscar_resposta_rag(pergunta, vectorstore)`**:
   - Use a **mesma lógica da Atividade 1**
   - vectorstore.similarity_search(pergunta, k=3)
   - Mesmo prompt estruturado
   - OpenAI Chat Completions
   - Retorne (resposta, docs)


## Como Executar o Template

### 1. Instalar Dependências
```bash
pip install streamlit PyPDF2 langchain langchain-openai langchain-community openai chromadb
```

### 2. Executar Aplicação
```bash
streamlit run atv_02.py
```

### 3. Usar Interface
1. Faça upload de um arquivo PDF
2. Clique em "Processar Documento"
3. Digite perguntas sobre o conteúdo
4. Visualize respostas e trechos consultados

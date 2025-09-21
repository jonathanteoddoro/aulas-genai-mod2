# Passo a passo – RAG Manual com Dados Mockados sobre Inteli Academy

### Pré-requisitos

1. **Instale as bibliotecas necessárias**:

```bash
pip install langchain openai chromadb
```

2. **Para executar o script**, execute no terminal:

```bash
python atv_01.py
```

---

### Passo a passo de implementação

1. **Configure a chave da OpenAI (topo do arquivo)**

   * Exemplo:

   ```python
   import os
   os.environ["OPENAI_API_KEY"] = "SUA_CHAVE_AQUI"
   ```

   * A chave será utilizada tanto para embeddings quanto para chamadas diretas à OpenAI.

2. **Prepare os dados mockados sobre Inteli Academy**

   * O código inclui 5 documentos detalhados sobre o Inteli Academy - Liga de IA.
   * Cada documento contém informações específicas sobre:
     - Visão geral da instituição e parcerias
     - Liga de IA e seus programas
     - Projetos desenvolvidos pelos estudantes
     - Metodologia PBL (Project Based Learning)
     - Infraestrutura e missão institucional

3. **Processamento de documentos e criação da base vetorial**

   * Use `CharacterTextSplitter` com `chunk_size=1000` e `chunk_overlap=200`
   * Crie embeddings usando `OpenAIEmbeddings()`
   * Armazene no `Chroma` (banco vetorial em memória)
   * Siga o padrão da aula: `Chroma.from_documents(texts, embeddings)`

4. **Implementação RAG Manual**

   * **Cliente OpenAI direto**: `client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])`
   * **Função de busca customizada**: `buscar_resposta_rag(pergunta, vectorstore)`
   * **Processo RAG**:
     - Busca documentos relevantes: `vectorstore.similarity_search(pergunta, k=3)`
     - Constrói contexto concatenando documentos
     - Cria prompt estruturado com instruções específicas
     - Faz chamada direta para `gpt-3.5-turbo`
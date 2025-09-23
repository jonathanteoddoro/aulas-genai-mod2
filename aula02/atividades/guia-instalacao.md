# Guia de Instalação - RAG Atividades

## 📋 Pré-requisitos
- Python 3.8+ instalado
- pip atualizado

## 🚀 Instalação Rápida

### 1️⃣ Criar Ambiente Virtual

**MacOS/Linux:**
```bash
cd aula02/atividades
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```cmd
cd aula02\atividades  
python -m venv .venv
.venv\Scripts\activate
```

### 2️⃣ Instalar Pacotes
```bash
pip install --upgrade pip
pip install streamlit PyPDF2 langchain langchain-openai langchain-community openai chromadb
```

### 3️⃣ Verificar Instalação
```bash
python -c "import streamlit, PyPDF2, langchain, openai; print('✅ Tudo instalado!')"
```

### 4️⃣ Para Executar Atividades

**Atividade 1 (Terminal):**
```bash
python atv_01.py
```

**Atividade 2 (Streamlit):**
```bash
streamlit run atv_02.py
```

## 🔑 Configuração OpenAI

1. Substitua `"sua_api_key_aqui"` nos arquivos Python

## 🛠️ Troubleshooting

**Desativar venv:**
```bash
deactivate
```

**Reativar venv:**
- MacOS/Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

## ✅ Checklist Final
- [ ] Python 3.8+ instalado
- [ ] venv criado e ativado  
- [ ] Pacotes instalados
- [ ] Chave OpenAI configurada
- [ ] Atividades executando

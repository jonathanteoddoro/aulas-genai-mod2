# Passo a passo – Assistente Multi-funções com Function Calling

### Pré-requisitos

1. **Instale as dependências necessárias:**
   ```bash
   pip install streamlit langchain langchain-openai
   ```

2. **Para rodar o app**, execute no terminal:
   ```bash
   streamlit run atv_02.py
   ```
   Acesse o link (Local URL) que aparece no seu terminal

---

## Objetivo do Exercício

Criar um assistente inteligente que **decide automaticamente** qual ferramenta usar baseado na pergunta do usuário. Isso é chamado de **Function Calling** - a IA analisa a intenção e escolhe a função apropriada.

---

## Passo a Passo

### **1. Coloque a chave da API (linha 13)**

* Exemplo:
  ```python
  OPENAI_API_KEY = "sk-proj-..."
  ```
* A chave fica no código para uso local (igual ao exercício anterior).

---

### **2. Implemente a função `obter_clima(cidade: str)`**

Esta função retorna informações simuladas sobre o clima de uma cidade.

**O que fazer:**
* Crie um dicionário com dados de clima de algumas cidades
* Use `.lower()` para tornar a busca case-insensitive
* Retorne uma string formatada com temperatura e condição

**Exemplo de estrutura:**
```python
climas = {
    "são paulo": {"temp": 25, "condicao": "Ensolarado", "umidade": 65},
    "rio de janeiro": {"temp": 30, "condicao": "Parcialmente nublado", "umidade": 75},
    "curitiba": {"temp": 18, "condicao": "Chuvoso", "umidade": 85},
    "salvador": {"temp": 28, "condicao": "Ensolarado", "umidade": 70}
}

cidade_lower = cidade.lower()
if cidade_lower in climas:
    info = climas[cidade_lower]
    return f"Clima em {cidade}: {info['temp']}°C, {info['condicao']}, Umidade: {info['umidade']}%"
else:
    return f"Desculpe, não tenho informações sobre o clima em {cidade}."
```

---

### **3. Implemente a função `converter_moeda(valor, moeda_origem, moeda_destino)`**

Esta função converte valores entre moedas usando taxas fixas simuladas.

**O que fazer:**
* Crie um dicionário com taxas de câmbio (use BRL como base = 1.0)
* Converta o valor primeiro para BRL, depois para a moeda de destino
* Normalize os códigos das moedas para maiúsculas
* Retorne uma string formatada com o resultado

**Exemplo de estrutura:**
```python
# Taxas em relação ao BRL
taxas = {
    "BRL": 1.0,
    "USD": 5.0,    # 1 USD = 5 BRL
    "EUR": 5.5,    # 1 EUR = 5.5 BRL
    "GBP": 6.3,    # 1 GBP = 6.3 BRL
    "JPY": 0.035   # 1 JPY = 0.035 BRL
}

moeda_origem = moeda_origem.upper()
moeda_destino = moeda_destino.upper()

# Verificar se as moedas existem
if moeda_origem not in taxas or moeda_destino not in taxas:
    return "Moeda não suportada. Moedas disponíveis: BRL, USD, EUR, GBP, JPY"

# Converter para BRL primeiro
valor_em_brl = valor * taxas[moeda_origem]

# Converter de BRL para moeda destino
valor_convertido = valor_em_brl / taxas[moeda_destino]

return f"{valor} {moeda_origem} = {valor_convertido:.2f} {moeda_destino}"
```

**Dica:** A conversão em duas etapas facilita adicionar novas moedas!

---

### **4. Implemente a função `calcular_imc(peso, altura)`**

Esta função calcula o IMC e retorna a classificação.

**O que fazer:**
* Calcule o IMC usando a fórmula: `IMC = peso / (altura ** 2)`
* Classifique o resultado de acordo com as faixas
* Retorne uma string formatada com o valor e a classificação

**Fórmula e classificações:**
```python
imc = peso / (altura ** 2)

# Classificações
if imc < 18.5:
    classificacao = "Abaixo do peso"
elif imc < 25:
    classificacao = "Peso normal"
elif imc < 30:
    classificacao = "Sobrepeso"
else:
    classificacao = "Obesidade"

return f"IMC: {imc:.1f} - Classificação: {classificacao}"
```

---

### **5. Adicione as ferramentas à lista (linha ~95)**

Depois de implementar todas as funções, você precisa registrá-las:

```python
tools = [
    obter_clima,
    converter_moeda,
    calcular_imc
]
```

**IMPORTANTE:** Se você esquecer de adicionar uma ferramenta aqui, o agente não conseguirá usá-la!

---

### **6. Execute e teste o agente**

O código já está configurado para:
* Criar o agente com as ferramentas
* Processar a pergunta do usuário
* Escolher automaticamente qual ferramenta usar
* Retornar a resposta formatada

**Você não precisa modificar mais nada!** O LangChain faz a mágica do function calling. 

## Conceitos Importantes

### O que é Function Calling?

Function calling permite que a IA:
1. **Entenda a intenção** do usuário
2. **Escolha a ferramenta certa** automaticamente
3. **Execute a função** com os parâmetros corretos
4. **Combine resultados** de múltiplas ferramentas se necessário

### Como funciona o decorator `@tool`?

```python
@tool
def minha_funcao(parametro: str) -> str:
    """
    Descrição clara do que a função faz.
    
    Args:
        parametro: Descrição do parâmetro
        
    Returns:
        Descrição do retorno
    """
    return "resultado"
```

**A docstring é CRUCIAL!** A IA lê a descrição para decidir quando usar a ferramenta.


## 🚀 Desafios Extras (Opcional)

Depois de completar o exercício básico, tente:

1. **Adicionar uma nova ferramenta:**
   * Calculadora de gorjeta
   * Conversor de temperatura (C ↔ F)
   * Gerador de senha aleatória

2. **Melhorar as ferramentas existentes:**
   * Adicionar mais cidades ao clima
   * Incluir mais moedas na conversão
   * Adicionar dicas de saúde no IMC

3. **Adicionar memória:**
   * Fazer o agente lembrar de conversas anteriores
   * Dica: use `ConversationBufferMemory` do LangChain

---

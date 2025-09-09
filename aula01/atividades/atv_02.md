# Passo a passo – Tradutor usando IA

### Pré-requisitos

1. **Para rodar o app**, execute no terminal:

```bash
streamlit run atv_01.py
```
Acesse o link (Local URL) que aparece no seu terminal


### Passo a Passo

1. **Coloque a chave local (topo do arquivo)**

   * Exemplo:

     ```python
     client = OpenAI(api_key="SUA_CHAVE_AQUI")
     ```
   * Aqui a chave fica no código mesmo (uso local).

2. **Receba o texto e o idioma alvo**

   * `texto`: o que o usuário digitou (`user_input`).
   * `idioma_destino`: o idioma escolhido (`idioma_alvo`).

3. **Monte o prompt para tradução**

   * Crie um texto que explique à IA o que fazer:

     * Informar o idioma de destino.
     * Pedir para **retornar só o texto traduzido**, sem explicações extras.
   * Exemplo de estrutura:

     ```
     "Traduza o seguinte texto para {idioma_destino}, apenas o texto: {texto}"
     ```

4. **Chame o endpoint da IA**

   * Parâmetros básicos que você precisa:

     * `model`: escolha um modelo de chat (ex: `"gpt-4o-mini"`).
     * `messages`: inclua o prompt como `role: "user"`.
     * `max_tokens`: controle de tamanho da resposta (ex: 512).
     * `temperature`: opcional, geralmente 0.3–0.7 para tradução.
   * Retorne a resposta que a IA gerar.

5. **Extraia apenas o texto traduzido**

   * Pegue de `resp.choices[0].message.content`.
   * Retorne apenas isso.
   * Trate caso a resposta seja nula ou ocorra algum erro simples.

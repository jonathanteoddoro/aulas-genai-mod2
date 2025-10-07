"""
Agente LangChain que recebe uma URL, utiliza uma ferramenta de scraping
para coletar o conteúdo da página e responde com um resumo.
"""

from __future__ import annotations

import os

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, AgentType, Tool, initialize_agent
from requests import RequestException

try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain.chat_models import ChatOpenAI


def scrape_website(url: str) -> str:
    """
    Extrai o texto principal de uma página HTML.

    - Remove scripts/estilos.
    - Retorna até 4000 caracteres para manter o contexto do modelo.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except RequestException as exc:
        raise ValueError(f"Falha ao acessar {url}: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove elementos não textuais para evitar ruído no resumo.
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text_content = " ".join(chunk.strip() for chunk in soup.stripped_strings)
    if not text_content:
        raise ValueError(f"O conteúdo em {url} está vazio ou não pôde ser processado.")

    return text_content[:4000]


def build_agent() -> AgentExecutor:
    """Constroi o agente LangChain configurado com a ferramenta de scraping."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Defina a variável de ambiente OPENAI_API_KEY (consulte o arquivo .env)."
        )

    llm = ChatOpenAI(temperature=0.2)

    tools = [
        Tool(
            name="WebsiteScraper",
            func=scrape_website,
            description=(
                "Use esta ferramenta para baixar o conteúdo textual bruto de uma página web. "
                "Informe a URL completa."
            ),
        )
    ]

    return initialize_agent(
        tools=tools,
        llm=llm,
        # verbose=True,
    )


def summarize_url(url: str) -> str:
    """Executa o agente pedindo um resumo da página informada."""
    agent = build_agent()
    prompt = (
        "Leia o conteúdo do site fornecido usando a ferramenta WebsiteScraper "
        "e produza um resumo em português, destacando os principais tópicos. "
        f"URL: {url}"
    )

    if hasattr(agent, "run"):
        return agent.run(prompt)

    result = agent.invoke({"input": prompt})

    return str(result)


def main() -> None:
    url = "https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line#removing-a-secret-introduced-by-an-earlier-commit-on-your-branch"  # Substitua pelo link que deseja resumir.
    summary = summarize_url(url)
    print(summary)


if __name__ == "__main__":
    main()

# Romulo RAG Chatbot

Este é um exemplo simples de chatbot em Flask que acumula conhecimento ao longo do tempo e utiliza um mecanismo de RAG (retrieval augmented generation) baseado em cadeias de Markov.

O conhecimento é armazenado em `data/knowledge.jsonl`. Cada nova linha adicionada representa um texto que poderá ser utilizado na geração de respostas.

## Como executar

Instale as dependências e execute o aplicativo Flask:

```bash
pip install -r requirements.txt
python -m romulo_rag.app
```

A aplicação ficará disponível em `http://localhost:5000`.

## Estrutura

- `knowledge_base.py` – Gerencia a base de conhecimento e realiza buscas por similaridade.
- `markov_generator.py` – Gera texto utilizando uma cadeia de Markov construída a partir dos textos recuperados.
- `rag.py` – Combina a busca com a geração para produzir uma resposta.
- `app.py` – Interface web via Flask com página de configuração.
- `config.py` – Gerencia o provedor de LLM e as chaves de API.

## Configurando LLMs

Acesse `/config` na aplicação para escolher entre os modelos **OpenAI**, **Claude**, **Qwen**, **Mistral** ou **Gemini**. Insira a chave de API correspondente e salve para que o chatbot utilize o provedor desejado. Caso nenhum provedor seja definido, o sistema utiliza a geração offline baseada em Markov.

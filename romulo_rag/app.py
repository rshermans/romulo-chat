from flask import Flask, request, jsonify, render_template_string

from .knowledge_base import KnowledgeBase
from .rag import generate_answer
from .config import AppConfig

app = Flask(__name__)
kb = KnowledgeBase("romulo_rag/data/knowledge.jsonl")
cfg = AppConfig("romulo_rag/data/config.json")


INDEX_HTML = """
<!doctype html>
<title>Romulo Chat</title>
<h1>Romulo Chatbot</h1>
<form action="/chat" method="post">
  <input name="message" style="width: 300px;" />
  <input type="submit" value="Send" />
</form>
<form action="/add" method="post" style="margin-top:20px;">
  <textarea name="text" rows="4" cols="50" placeholder="Add knowledge"></textarea><br>
  <input type="submit" value="Add" />
</form>
<p><a href="/config">Configura\u00e7\u00f5es</a></p>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "")
    answer = generate_answer(message, kb, config=cfg)
    return render_template_string(
        INDEX_HTML
        + f"<p><b>Você:</b> {message}</p><p><b>Romulo:</b> {answer}</p>"
    )


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "")
    kb.add_document(text)
    return render_template_string(INDEX_HTML + "<p>Knowledge added.</p>")


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    message = data.get("message", "")
    answer = generate_answer(message, kb)
    return jsonify({"response": answer})


CONFIG_HTML = """
<h2>Configura\u00e7\u00e3o do Chatbot</h2>
<form method="post">
  <label>Modelo:</label>
  <select name="provider">
    <option value="markov">Markov (offline)</option>
    <option value="openai">OpenAI</option>
    <option value="claude">Claude</option>
    <option value="qwen">Qwen</option>
    <option value="mistral">Mistral</option>
    <option value="gemini">Gemini</option>
  </select><br>
  <label>API Key:</label>
  <input name="api_key" style="width:300px"/><br>
  <input type="submit" value="Salvar"/>
</form>
"""


@app.route("/config", methods=["GET", "POST"])
def config_page():
    if request.method == "POST":
        provider = request.form.get("provider", "markov")
        api_key = request.form.get("api_key", "").strip()
        cfg.set_provider(provider)
        if api_key:
            cfg.set_api_key(provider, api_key)
        return render_template_string(
            CONFIG_HTML + "<p>Configura\u00e7\u00e3o salva.</p>"
        )
    return render_template_string(CONFIG_HTML)


if __name__ == "__main__":
    app.run(debug=True)

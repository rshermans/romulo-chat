from flask import Flask, request, jsonify, render_template_string

from .knowledge_base import KnowledgeBase
from .rag import generate_answer

app = Flask(__name__)
kb = KnowledgeBase("romulo_rag/data/knowledge.jsonl")


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
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)


@app.route("/chat", methods=["POST"])
def chat():
    message = request.form.get("message", "")
    answer = generate_answer(message, kb)
    return render_template_string(INDEX_HTML + f"<p><b>Você:</b> {message}</p><p><b>Romulo:</b> {answer}</p>")


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


if __name__ == "__main__":
    app.run(debug=True)

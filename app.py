from flask import Flask, render_template, request, jsonify
from rag import answer_question

app = Flask(__name__)


@app.route("/")
def home():
    """Display the PythonBookAI home page."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """Accept a question and return the RAG answer."""

    data = request.get_json(silent=True) or {}

    question = data.get("question", "").strip()
    source = data.get("source")
    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    try:
        result = answer_question(
    question,
    source=source
)

        sources = []

        for source in result.get("sources", []):
            sources.append({
                "book": source.get("source", "Unknown"),
                "page": source.get("page", "Unknown")
            })

        return jsonify({
            "answer": result["answer"],
            "sources": sources,
            "code_validation": result.get(
                "code_validation", {}
            )
        })

    except Exception:
        app.logger.exception("Question processing failed")

        return jsonify({
            "error": (
                "Sorry, I couldn't process your question. "
                "Check the terminal for details."
            )
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
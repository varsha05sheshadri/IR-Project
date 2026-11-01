from flask import Flask, render_template, request, abort, Response
from pathlib import Path
import json, csv, io, sqlite3
from datetime import datetime
from search_engine import LegalSearchEngine

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
app.config["SECRET_KEY"] = "change-this-for-production"
DATA = json.loads((ROOT / "dataset.json").read_text(encoding="utf-8"))
engine = LegalSearchEngine(DATA)
DB_PATH = ROOT / "search_history.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            result_count INTEGER NOT NULL,
            searched_at TEXT NOT NULL
        )""")
init_db()

def get_categories():
    return sorted({item["category"] for item in DATA})

@app.route("/", methods=["GET"])
def index():
    recent = []
    with sqlite3.connect(DB_PATH) as conn:
        recent = conn.execute(
            "SELECT query, result_count, searched_at FROM searches ORDER BY id DESC LIMIT 5"
        ).fetchall()
    return render_template("index.html", categories=get_categories(), recent=recent)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    if not query:
        return render_template("results.html", query=query, results=[], category=category,
                               message="Enter a word or phrase to search.", categories=get_categories())
    results = engine.search(query, category=category)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO searches(query, result_count, searched_at) VALUES (?, ?, ?)",
                     (query, len(results), datetime.now().strftime("%d %b %Y, %I:%M %p")))
    return render_template("results.html", query=query, results=results, category=category,
                           message="No matching sections found. Try another keyword." if not results else "",
                           categories=get_categories())

@app.route("/document/<int:doc_id>")
def document(doc_id):
    item = next((d for d in DATA if d["id"] == doc_id), None)
    if item is None:
        abort(404)
    return render_template("document.html", item=item)

@app.route("/export")
def export():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    results = engine.search(query, category=category) if query else []
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Act", "Section", "Title", "Category", "Relevance score", "Summary", "Official source"])
    for r in results:
        writer.writerow([r["act"], r["section"], r["title"], r["category"],
                         f'{r["score"]:.4f}', r["text"], r["source"]])
    return Response("\ufeff" + output.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=legal-search-results.csv"})

@app.route("/history")
def history():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT query, result_count, searched_at FROM searches ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return render_template("history.html", rows=rows)

@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run(debug=True)

# IR PROJECT — Legal Document Search System

A beginner-friendly Information Retrieval (IR) web application. Users search a small prepared collection of Indian legal provision summaries. The system ranks matching sections with **TF-IDF** and **cosine similarity**, then lets users read a section overview and open its source.

## Features
- Search by keyword or phrase
- TF-IDF + cosine similarity ranking
- Filter by legal category
- Result snippets and similarity scores
- Section detail page and source links
- Recent search history stored in SQLite
- Export search results to CSV
- Responsive HTML/CSS interface

## Requirements
- Python 3.10 or newer
- pip

## Run on Windows
1. Extract the ZIP.
2. Open the extracted `IR PROJECT` folder in VS Code.
3. Open a terminal in that folder.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv venv
   .\venv\Scripts\activate
   ```

5. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python app.py
   ```

7. Open **http://127.0.0.1:5000** in your browser.

## Run on macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Then open http://127.0.0.1:5000.

## How the search works
1. The application loads `dataset.json`.
2. `TfidfVectorizer` converts each legal section's text and metadata into a TF-IDF vector.
3. The user's query is transformed using the same vectorizer.
4. Cosine similarity compares the query vector with every section vector.
5. Matching sections are sorted from highest to lowest similarity.

A similarity score is a ranking signal, **not** a probability that a legal interpretation is correct.

## Project files
- `app.py` — Flask routes, history database and CSV export
- `search_engine.py` — information retrieval implementation
- `dataset.json` — prepared sample legal dataset
- `templates/` — HTML pages
- `static/style.css` — responsive styling
- `requirements.txt` — Python dependencies

## Dataset note — please read
The included 15 entries are **short educational summaries**, not complete or verbatim statutory sections. Source links point to official government legislation portals. Before an academic/public release, verify every section against the current official text, add the exact document/section URLs where available, and expand the dataset. The app is a search demonstration, not a legal advice tool.

## Troubleshooting
- If `pip` is not recognised, use `py -m pip install -r requirements.txt`.
- If port 5000 is busy, change the final line in `app.py` to `app.run(debug=True, port=5001)` and visit port 5001.
- If dependencies fail to install, check that Python 3.10+ is installed and the virtual environment is active.

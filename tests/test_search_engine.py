import json
from pathlib import Path
from search_engine import LegalSearchEngine

DATA = json.loads((Path(__file__).resolve().parents[1] / "dataset.json").read_text(encoding="utf-8"))

def test_search_returns_identity_theft_section():
    results = LegalSearchEngine(DATA).search("identity theft")
    assert results
    assert results[0]["section"] == "66C"

def test_category_filter():
    results = LegalSearchEngine(DATA).search("privacy", category="Privacy")
    assert results
    assert all(item["category"] == "Privacy" for item in results)

def test_empty_query_returns_no_results():
    assert LegalSearchEngine(DATA).search("   ") == []

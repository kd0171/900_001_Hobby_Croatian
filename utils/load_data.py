import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REFERENCES_DIR = DATA_DIR / "references"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_all_data():
    vocabulary = load_json(DATA_DIR / "vocabulary.json")
    sentences = load_json(DATA_DIR / "sentences.json")
    dialogues = load_json(DATA_DIR / "dialogues.json")
    references = {}
    for path in sorted(REFERENCES_DIR.glob("*.json")):
        data = load_json(path)
        references[data["id"]] = data
    return {
        "vocabulary": vocabulary,
        "sentences": sentences,
        "dialogues": dialogues,
        "references": references,
    }

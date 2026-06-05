import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REFERENCES_DIR = DATA_DIR / "references"

COLLECTION_FILES = {
    "vocabulary": DATA_DIR / "vocabulary.json",
    "sentences": DATA_DIR / "sentences.json",
    "dialogues": DATA_DIR / "dialogues.json",
}
COLLECTION_DIRS = {
    "vocabulary": DATA_DIR / "vocabulary",
    "sentences": DATA_DIR / "sentences",
    "dialogues": DATA_DIR / "dialogues",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _as_list(data: Any) -> list:
    """Allow either a plain list or {"items": [...]} / {"sentences": [...]} style files."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ["items", "vocabulary", "sentences", "dialogues"]:
            if isinstance(data.get(key), list):
                return data[key]
    raise ValueError("JSON collection must be a list or a dict containing an item list.")


def load_collection(name: str) -> list:
    """Load built-in JSON plus every *.json in data/<name>/.

    This makes the app extendable: add a new file such as
    data/sentences/my_new_lesson.json and restart the app.
    """
    items = []
    base_file = COLLECTION_FILES[name]
    if base_file.exists():
        items.extend(_as_list(load_json(base_file)))

    extra_dir = COLLECTION_DIRS[name]
    if extra_dir.exists():
        for path in sorted(extra_dir.glob("*.json")):
            items.extend(_as_list(load_json(path)))

    # Keep the first item when duplicate ids exist. This avoids accidental duplicate cards.
    seen = set()
    deduped = []
    for item in items:
        item_id = item.get("id") if isinstance(item, dict) else None
        if item_id and item_id in seen:
            continue
        if item_id:
            seen.add(item_id)
        deduped.append(item)
    return deduped


def load_references() -> dict:
    references = {}
    if REFERENCES_DIR.exists():
        for path in sorted(REFERENCES_DIR.glob("*.json")):
            data = load_json(path)
            references[data["id"]] = data
    return references


def load_all_data():
    return {
        "vocabulary": load_collection("vocabulary"),
        "sentences": load_collection("sentences"),
        "dialogues": load_collection("dialogues"),
        "references": load_references(),
    }

import re
import unicodedata

CROATIAN_MAP = str.maketrans({
    "č": "c", "ć": "c", "š": "s", "ž": "z", "đ": "d",
    "Č": "c", "Ć": "c", "Š": "s", "Ž": "z", "Đ": "d",
})


def normalize_text(text: str, strict_diacritics: bool = False) -> str:
    """Normalize answer text for beginner-friendly checking."""
    if text is None:
        return ""
    text = str(text).strip().lower()
    text = unicodedata.normalize("NFC", text)
    if not strict_diacritics:
        text = text.translate(CROATIAN_MAP)
    text = re.sub(r"[\.,!?¡¿;:、。！？]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

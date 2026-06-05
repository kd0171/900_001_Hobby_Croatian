from .text_normalizer import normalize_text


def filter_by_scene_and_level(items, scenes, max_level):
    scenes = set(scenes or [])
    result = []
    for item in items:
        if scenes and item.get("scene") not in scenes:
            continue
        if int(item.get("level", 1)) > int(max_level):
            continue
        result.append(item)
    return result


def check_answer(user_answer, accepted_answers, strict_diacritics=False):
    user_norm = normalize_text(user_answer, strict_diacritics=strict_diacritics)
    accepted_norm = [normalize_text(a, strict_diacritics=strict_diacritics) for a in accepted_answers]
    return user_norm in accepted_norm

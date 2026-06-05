# 教材JSONスキーマ

## 1. Vocabulary

保存先：

```text
data/vocabulary/*.json
```

形式：配列、または `{ "items": [...] }`。

主なフィールド：

```json
{
  "id": "zadar_seafood_01",
  "scene": "fish_market",
  "level": 1,
  "hr": "brancin",
  "ja": "ヨーロピアンシーバス（スズキに似た白身魚）",
  "pronunciation_ja": "ブランツィン",
  "part_of_speech": "noun",
  "gender": "masculine",
  "tags": ["seafood", "zadar"],
  "examples": [
    {
      "hr": "Je li ovaj brancin svjež?",
      "pronunciation_ja": "イェ リ オヴァイ ブランツィン スヴィェジュ",
      "ja": "このブランジーノは新鮮ですか？"
    }
  ],
  "grammar": {
    "note_ja": "文法メモ",
    "declension": [],
    "prepositional_examples": []
  }
}
```

## 2. Sentences

保存先：

```text
data/sentences/*.json
```

主なフィールド：

```json
{
  "id": "zadar_fish_sentence_01",
  "scene": "fish_market",
  "level": 2,
  "ja": "この魚を三枚おろしにできますか？",
  "hr": "Možete li ovu ribu filetirati?",
  "pronunciation_ja": "モジェテ リ オヴ リブ フィレティラティ",
  "tokens": [
    {"hr": "Možete li", "pronunciation_ja": "モジェテ リ", "meaning_ja": "〜してもらえますか"}
  ],
  "grammar": {
    "title": "丁寧依頼",
    "explanation_ja": "Možete li...? は丁寧な依頼。",
    "tables": [],
    "notes": []
  }
}
```

## 3. Dialogues

保存先：

```text
data/dialogues/*.json
```

主なフィールド：

```json
{
  "id": "fish_story_fillet",
  "scene": "fish_market",
  "level": 2,
  "title_ja": "魚市場-三枚おろし",
  "dialogue": [
    {
      "speaker": "A",
      "hr": "Možete li ovu ribu filetirati?",
      "pronunciation_ja": "モジェテ リ オヴ リブ フィレティラティ",
      "ja": "この魚を三枚おろしにできますか？"
    }
  ],
  "vocabulary_notes": [
    {
      "hr": "filetirati",
      "pronunciation_ja": "フィレティラティ",
      "meaning_ja": "三枚おろし・フィレにする",
      "note_ja": "fillet に相当。"
    }
  ],
  "seafood_table": [],
  "grammar_notes": [],
  "questions": []
}
```

## 4. References

保存先：

```text
data/references/*.json
```

形式：

```json
{
  "id": "seafood_zadar",
  "title_ja": "ザダル魚介類",
  "title_hr": "Ribe i morski plodovi u Zadru",
  "sections": [
    {
      "id": "common_market_fish",
      "title_ja": "魚市場で見やすい魚介類",
      "note_ja": "説明",
      "items": [
        {
          "ja": "ヨーロピアンシーバス（スズキに似た白身魚）",
          "hr": "brancin / lubin",
          "pronunciation_ja": "ブランツィン / ルビン",
          "note_ja": "メモ"
        }
      ],
      "examples": []
    }
  ]
}
```

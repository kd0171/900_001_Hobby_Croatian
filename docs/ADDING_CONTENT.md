# 教材追加の方法

このアプリは、既存のアプリ本体を変更しなくても教材を追加できるようにしています。
新しいJSONファイルを以下のフォルダに追加して、アプリを再起動してください。

```text
data/vocabulary/*.json
data/sentences/*.json
data/dialogues/*.json
data/references/*.json
```

既存の以下のファイルも引き続き読み込まれます。

```text
data/vocabulary.json
data/sentences.json
data/dialogues.json
```

読み込み順は、まず既存の単体JSON、その後に各フォルダ内のJSONです。`id` が重複した場合は、最初に読み込まれた項目が優先されます。

## 追加用JSONの基本形

各追加ファイルは、次のどちらの形式でも読み込めます。

### 形式A: 配列そのもの

```json
[
  {
    "id": "sentence_my_001",
    "scene": "supermarket",
    "level": 1,
    "ja": "水をください。",
    "hr": "Vodu, molim.",
    "pronunciation_ja": "ヴォドゥ モリム"
  }
]
```

### 形式B: itemsで包む形式

```json
{
  "items": [
    {
      "id": "sentence_my_001",
      "scene": "supermarket",
      "level": 1,
      "ja": "水をください。",
      "hr": "Vodu, molim.",
      "pronunciation_ja": "ヴォドゥ モリム"
    }
  ]
}
```

## scene の候補

```text
basic
sea
boat
supermarket
fish_market
sea_urchin
tourism
```

## vocabulary の最小例

```json
{
  "id": "vocab_my_word_001",
  "scene": "supermarket",
  "level": 1,
  "hr": "voda",
  "ja": "水",
  "pronunciation_ja": "ヴォダ",
  "part_of_speech": "noun",
  "gender": "feminine",
  "tags": ["supermarket", "noun"],
  "examples": [
    {
      "hr": "Vodu, molim.",
      "pronunciation_ja": "ヴォドゥ モリム",
      "ja": "水をください。"
    }
  ],
  "grammar": {
    "note_ja": "女性名詞です。旅行では対格 vodu がよく出ます。",
    "declension": [
      {"case_ja":"主格","case_hr":"nominativ","singular":"voda","plural":"vode","main_use_ja":"主語"},
      {"case_ja":"属格","case_hr":"genitiv","singular":"vode","plural":"voda","main_use_ja":"〜の、数量の後"},
      {"case_ja":"与格","case_hr":"dativ","singular":"vodi","plural":"vodama","main_use_ja":"〜へ、〜に"},
      {"case_ja":"対格","case_hr":"akuzativ","singular":"vodu","plural":"vode","main_use_ja":"目的語"},
      {"case_ja":"呼格","case_hr":"vokativ","singular":"vodo","plural":"vode","main_use_ja":"呼びかけ"},
      {"case_ja":"処格","case_hr":"lokativ","singular":"vodi","plural":"vodama","main_use_ja":"場所、前置詞の後"},
      {"case_ja":"具格","case_hr":"instrumental","singular":"vodom","plural":"vodama","main_use_ja":"〜で"}
    ],
    "prepositional_examples": [
      {
        "phrase_hr": "s vodom",
        "pronunciation_ja": "ス ヴォドム",
        "meaning_ja": "水と一緒に／水付きで",
        "note_ja": "s + 具格の例です。"
      }
    ]
  }
}
```

## sentence の最小例

```json
{
  "id": "sentence_my_001",
  "scene": "supermarket",
  "level": 1,
  "ja": "水をください。",
  "hr": "Vodu, molim.",
  "pronunciation_ja": "ヴォドゥ モリム",
  "tags": ["supermarket", "request"],
  "tokens": [
    {"hr": "Vodu", "pronunciation_ja": "ヴォドゥ", "meaning_ja": "水を"},
    {"hr": "molim", "pronunciation_ja": "モリム", "meaning_ja": "お願いします"}
  ],
  "accepted_answers_hr": ["Vodu, molim.", "Vodu molim"],
  "accepted_answers_ja": ["水をください。", "水をください"],
  "grammar": {
    "title": "目的語の形",
    "explanation_ja": "voda は女性名詞で、ここでは目的語なので vodu になります。",
    "tables": [
      {
        "title_ja": "形の確認",
        "headers": ["form", "role", "meaning"],
        "header_labels": {"form":"形", "role":"役割", "meaning":"意味"},
        "rows": [
          {"form":"voda", "role":"主格", "meaning":"水が"},
          {"form":"vodu", "role":"対格", "meaning":"水を"}
        ]
      }
    ],
    "notes": ["molim は旅行会話で非常によく使う丁寧表現です。"]
  }
}
```

## dialogue の最小例

```json
{
  "id": "dialogue_my_001",
  "scene": "supermarket",
  "level": 1,
  "title_ja": "スーパーで水を買う",
  "title_hr": "Kupnja vode",
  "dialogue": [
    {
      "speaker": "A",
      "hr": "Dobar dan. Vodu, molim.",
      "pronunciation_ja": "ドバル ダン ヴォドゥ モリム",
      "ja": "こんにちは。水をください。"
    },
    {
      "speaker": "B",
      "hr": "Izvolite.",
      "pronunciation_ja": "イズヴォリテ",
      "ja": "どうぞ。"
    }
  ],
  "questions": [
    {
      "id": "q1",
      "type": "multiple_choice",
      "question_ja": "Aさんは何を買っていますか？",
      "choices_ja": ["水", "魚", "チケット", "薬"],
      "answer": "水"
    }
  ],
  "grammar_notes": [
    {
      "title_ja": "Vodu, molim.",
      "explanation_ja": "水をください、という短い依頼表現です。"
    }
  ]
}
```

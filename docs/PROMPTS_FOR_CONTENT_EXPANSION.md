# 今後の教材追加用プロンプト例

## 1. 例文追加

```text
クロアチア旅行アプリ用に、scene="fish_market"、level=2 の例文を20個作成してください。
各項目には id, scene, level, ja, hr, pronunciation_ja, tokens, grammar, accepted_answers_hr, accepted_answers_ja を含めてください。
JSON配列のみで出力してください。
日本語話者向けに、カタカナ発音は単語ごとに空白で区切ってください。
```

## 2. 対話読解追加

```text
クロアチア旅行アプリ用に、魚市場で魚を買う対話読解を5件作成してください。
各タイトルは日本語14文字以内にしてください。
各対話には dialogue, vocabulary_notes, seafood_table, grammar_notes, questions を含めてください。
魚名は brancin だけでなく、日本語で「スズキに似た白身魚」のように説明してください。
JSON配列のみで出力してください。
```

## 3. 参考ページ追加

```text
data/references に追加するJSONとして、クロアチア語のレストラン表現ページを作成してください。
id, title_ja, title_hr, sections を持つ形式にしてください。
itemsには ja, hr, pronunciation_ja, note_ja を含めてください。
examples も各sectionに付けてください。
```

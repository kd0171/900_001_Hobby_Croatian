# 教材を増やすためのプロンプト例

以下をChatGPTなどに貼り付けると、アプリに追加しやすいJSON教材を作れます。
生成結果は `data/sentences/追加名.json` や `data/vocabulary/追加名.json` に保存してください。

```text
日本語話者向けの初級クロアチア語旅行学習アプリ用に、JSON教材を作成してください。

条件:
- scene は basic, sea, boat, supermarket, fish_market, sea_urchin, tourism のいずれか
- level は 1〜3
- すべてのクロアチア語文にカタカナ発音を付ける
- 文の場合、カタカナ発音は単語ごとに空白で区切る
- 各 sentence には tokens, accepted_answers_hr, accepted_answers_ja, grammar を付ける
- grammar.tables には、文型・格変化・動詞変化・数量表現など、該当する表を最低1つ入れる
- 返答はJSONだけにする
- 形式は {"items": [...]} にする

作成内容:
- scene: fish_market
- 例文: 20文
- 内容: 魚市場で量り売りの魚を買う、生食可能か確認する、氷を頼む、値段を聞く
```

## 注意

生成されたクロアチア語・活用・格変化は、必要に応じて辞書やネイティブ確認で精度を上げてください。特に生食・採集・規則に関わる内容は、言語表現だけでなく現地ルールの確認が必要です。
```

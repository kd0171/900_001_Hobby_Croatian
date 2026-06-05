# Croatian Travel Phrase Trainer

Plotly Dashで作成した、夏のクロアチア旅行向けの初級クロアチア語学習アプリです。
SQLiteなどのDBは使わず、教材はJSONで管理します。

## 起動方法

```bash
conda create -n croatian-travel-app python=3.11
conda activate croatian-travel-app
pip install -r requirements.txt
python app.py
```

ブラウザで以下を開きます。

```text
http://127.0.0.1:8050
```

## 主な機能

- 単語学習
  - シーン別チェックボックス
  - 名詞・動詞・形容詞・副詞などの品詞フィルタ
  - 20件ずつ一覧表示
  - 各単語に例文を表示
  - 折り畳みで格変化・動詞変化・語形変化を確認
- 例文学習
  - 20件ずつ一覧表示
  - 各例文にカタカナ発音
  - 折り畳みで単語分解・文法解説を確認
- 四択クイズ
  - ヒントや正解後確認は最初から表示せず、回答後に表示
- 入力クイズ
  - 発音ヒントはボタンを押したときだけ表示
  - 正解後確認は回答後に表示
- 対話読解
  - シーン別の短い対話
  - 日本語訳・文法メモは折り畳み表示
- 参考ページ
  - 数字、曜日、月、時間、単位、疑問詞

## 教材データ

```text
data/
  vocabulary.json
  sentences.json
  dialogues.json
  references/
    numbers.json
    weekdays.json
    months.json
    time.json
    units.json
    question_words.json
```

## 学習履歴について

現時点では学習履歴保存は実装していません。
まずはUIと教材表示を優先したMVPです。

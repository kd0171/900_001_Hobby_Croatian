# Croatian Travel Phrase Trainer

Plotly Dashで作成した、日本語話者向けの初級クロアチア語旅行表現アプリです。
SQLiteなどのDBは使わず、教材はすべて `data/*.json` と `data/references/*.json` から読み込みます。

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

- 単語学習：20件ずつ縦一覧表示、品詞フィルタ、カード内スクロール
- 例文学習：20件ずつ縦一覧表示、単語分解、文法表、補足メモ
- 四択クイズ：回答後のみ正解確認を表示
- 入力クイズ：発音ヒントはボタンを押した時のみ表示
- 対話読解：シーン別の短い会話と読解問題
- 参考ページ：数字、曜日、月、時間、日付、単位、疑問詞

## データ追加

教材追加はJSONを編集します。

- `data/vocabulary.json`: 単語、発音、例文、格変化・動詞変化
- `data/sentences.json`: 例文、単語分解、文法表
- `data/dialogues.json`: 対話文と読解問題
- `data/references/*.json`: 参考ページ

## 注意

カタカナ発音は日本語話者向けの近似です。クロアチア語の č / ć / š / ž / đ / lj / nj / r などはカタカナだけでは完全には表せません。

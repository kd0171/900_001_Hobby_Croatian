# Croatian Travel Phrase Trainer

Plotly Dashで実装した、日本語話者向けの初級クロアチア語旅行表現アプリです。
SQLiteなどのDBは使わず、教材はJSONから読み込みます。

## 主な機能

- 単語学習：20件ずつ縦スクロール一覧表示
- 単語の品詞フィルタ：名詞、動詞、形容詞、副詞、疑問詞、数詞など
- 単語カード内の折り畳み表示：例文、格変化、動詞変化、前置詞句例
- 例文学習：20件ずつ縦スクロール一覧表示
- 例文カード内の折り畳み表示：単語分解、文法表、補足メモ
- 四択クイズ
- 入力クイズ
- 対話読解：タイトルのドロップダウンから選択可能
- 参考ページ：数字、曜日、月、時間、日付、単位、疑問詞
- 控えめなクロアチア国旗イメージのデザイン

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

## データ追加

教材は以下のJSONを編集・追加することで拡張できます。

```text
data/vocabulary.json
data/sentences.json
data/dialogues.json
data/references/*.json
```

学習履歴保存は実装していません。

# 魚市場・魚介類語彙の追加方針

## 目的

魚市場で実際に量り売りの魚介類を買う場面を想定し、単なる魚名の暗記ではなく、以下を言えるようにする。

- 魚介類の名前を理解する
- 日本語と完全対応しない魚名は「〜に似た魚」として理解する
- マグロの部位を、トロ・赤身・血合いのような日本語中心の語彙ではなく、現地で説明しやすい表現に置き換える
- 下処理・切り方・避けたい部分を店員に確認する

## マグロの部位表現

日本語の「赤身」「中トロ」「大トロ」「血合い」は、クロアチア語の魚市場で常にそのまま対応語があるとは限らない。
そのため、このアプリでは次のように説明型の語彙を優先する。

| 日本語で言いたいこと | クロアチア語表現 | 考え方 |
|---|---|---|
| マグロ | tuna | 基本語彙 |
| クロマグロ系 | plavoperajna tuna | 魚種確認用 |
| トロに近い部分 | masniji dio tune | 脂の多い部分 |
| 腹側 | trbušni dio tune | 脂が多い部位を位置で説明 |
| 白っぽい脂の多い部分 | svjetliji i masniji dio | 見た目で説明 |
| 血合い周り | tamni dio uz krvnu liniju | 暗い部分・血のラインの近く |
| 血合いを避けたい | Bez tamnog dijela, molim. | 簡潔な依頼表現 |

## データ配置

今回追加した内容は以下に分けている。

```text
data/vocabulary/tuna_shrimp_squid_octopus_vocab.json
data/sentences/tuna_shrimp_squid_octopus_sentences.json
data/dialogues/tuna_shrimp_squid_octopus_dialogues.json
data/references/seafood_zadar.json
```

## 今後の追加方法

魚介類や市場表現を追加する場合は、アプリ本体ではなく、上記と同じ形式の JSON を `data/vocabulary/`, `data/sentences/`, `data/dialogues/` に追加する。
アプリは起動時に `*.json` を自動読み込みする。

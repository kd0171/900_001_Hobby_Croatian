from __future__ import annotations

import math
import random
from typing import Any, Dict, List

import dash
from dash import Dash, Input, Output, State, dcc, html
import dash_bootstrap_components as dbc

from utils.load_data import load_all_data
from utils.quiz_logic import filter_by_scene_and_level, check_answer

DATA = load_all_data()

SCENES = [
    {"label": "基本表現", "value": "basic"},
    {"label": "海", "value": "sea"},
    {"label": "船", "value": "boat"},
    {"label": "スーパー", "value": "supermarket"},
    {"label": "魚市場", "value": "fish_market"},
    {"label": "ウニ・海の生き物", "value": "sea_urchin"},
    {"label": "観光", "value": "tourism"},
]

MODES = [
    {"label": "単語学習", "value": "vocab"},
    {"label": "例文学習", "value": "sentences"},
    {"label": "四択クイズ", "value": "multiple_choice"},
    {"label": "入力クイズ", "value": "input_quiz"},
    {"label": "対話読解", "value": "dialogue"},
    {"label": "参考ページ", "value": "reference"},
]

DIRECTIONS = [
    {"label": "日本語 → クロアチア語", "value": "ja_to_hr"},
    {"label": "クロアチア語 → 日本語", "value": "hr_to_ja"},
]

REFERENCE_OPTIONS = [
    {"label": v["title_ja"], "value": k}
    for k, v in DATA["references"].items()
    if k != "weekdays"
]

POS_LABELS = {
    "noun": "名詞",
    "verb": "動詞",
    "adjective": "形容詞",
    "adverb": "副詞",
    "phrase": "定型表現",
    "question_word": "疑問詞",
    "number": "数詞",
    "preposition": "前置詞",
    "other": "その他",
}

POS_OPTIONS = []
for pos in sorted({v.get("part_of_speech", "other") for v in DATA["vocabulary"]}):
    POS_OPTIONS.append({"label": POS_LABELS.get(pos, pos), "value": pos})

ITEMS_PER_PAGE = 20


def short_ja_title(title: str, max_chars: int = 14) -> str:
    """Keep mobile dropdown/card titles short and Japanese-only."""
    title = (title or "").replace("／", "-").replace("/", "-").strip()
    if len(title) <= max_chars:
        return title
    return title[:max_chars - 1] + "…"


def section_examples(examples: List[Dict[str, str]] | None):
    if not examples:
        return None
    rows = [html.Tr([html.Th("日本語"), html.Th("クロアチア語"), html.Th("カタカナ"), html.Th("メモ")])]
    for ex in examples:
        rows.append(html.Tr([
            html.Td(ex.get("ja", "")),
            html.Td(ex.get("hr", "")),
            html.Td(ex.get("pronunciation_ja", "")),
            html.Td(ex.get("note_ja", "")),
        ]))
    return html.Div([
        html.H5("例文"),
        dbc.Table(rows, bordered=True, hover=True, responsive=True, className="reference-table examples-table"),
    ], className="reference-examples")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server


def card_header(title: str, subtitle: str | None = None):
    return html.Div([
        html.H3(title, className="card-title-main"),
        html.Div(subtitle, className="muted") if subtitle else None,
    ])


def render_key_value_table(rows: List[Dict[str, str]], headers: List[str] | None = None, header_labels: Dict[str, str] | None = None):
    if not rows:
        return html.Div("未登録です。", className="muted")
    headers = headers or list(rows[0].keys())
    header_labels = header_labels or {}
    table_rows = [html.Tr([html.Th(header_labels.get(h, h)) for h in headers])]
    for row in rows:
        table_rows.append(html.Tr([html.Td(row.get(h, "")) for h in headers]))
    return dbc.Table(table_rows, bordered=True, hover=True, responsive=True, className="small-table")


def render_tokens(tokens: List[Dict[str, str]] | None):
    if not tokens:
        return html.Div("単語ごとの情報は未登録です。", className="muted")
    rows = [html.Tr([html.Th("単語"), html.Th("カタカナ"), html.Th("意味")])]
    for t in tokens:
        rows.append(html.Tr([
            html.Td(t.get("hr", "")),
            html.Td(t.get("pronunciation_ja", "")),
            html.Td(t.get("meaning_ja", "")),
        ]))
    return dbc.Table(rows, bordered=True, hover=True, responsive=True, className="small-table")

def render_dialogue_vocab_notes(notes: List[Dict[str, str]] | None):
    if not notes:
        return html.Div("この読解の単語解説は未登録です。", className="muted")
    rows = [html.Tr([html.Th("語句"), html.Th("カタカナ"), html.Th("意味"), html.Th("メモ")])]
    for n in notes:
        rows.append(html.Tr([
            html.Td(n.get("hr", "")),
            html.Td(n.get("pronunciation_ja", "")),
            html.Td(n.get("meaning_ja", n.get("ja", ""))),
            html.Td(n.get("note_ja", "")),
        ]))
    return dbc.Table(rows, bordered=True, hover=True, responsive=True, className="small-table dialogue-vocab-table")


def render_seafood_table(items: List[Dict[str, str]] | None):
    if not items:
        return None
    rows = [html.Tr([html.Th("クロアチア語"), html.Th("カタカナ"), html.Th("日本語での理解"), html.Th("メモ")])]
    for item in items:
        rows.append(html.Tr([
            html.Td(item.get("hr", "")),
            html.Td(item.get("pronunciation_ja", "")),
            html.Td(item.get("meaning_ja", item.get("ja", ""))),
            html.Td(item.get("note_ja", "")),
        ]))
    return dbc.Table(rows, bordered=True, hover=True, responsive=True, className="small-table seafood-table")


def pos_badge(item: Dict[str, Any]):
    pos = item.get("part_of_speech", "other")
    label = POS_LABELS.get(pos, pos)
    return dbc.Badge(label, color="secondary", className="me-1")


def render_inflection_block(item: Dict[str, Any]):
    grammar = item.get("grammar", {})
    blocks = []
    if grammar.get("note_ja"):
        blocks.append(html.P(grammar["note_ja"], className="mb-2"))
    if grammar.get("declension"):
        blocks.append(html.H6("格変化：単数・複数の全7格"))
        blocks.append(render_key_value_table(
            grammar["declension"],
            ["case_ja", "case_hr", "singular", "plural", "main_use_ja"],
            {"case_ja":"格", "case_hr":"クロアチア語名", "singular":"単数", "plural":"複数", "main_use_ja":"主な使い方"}
        ))
    if grammar.get("prepositional_examples"):
        blocks.append(html.H6("代表的な前置詞との組み合わせ"))
        blocks.append(render_key_value_table(
            grammar["prepositional_examples"],
            ["phrase_hr", "pronunciation_ja", "meaning_ja", "note_ja"],
            {"phrase_hr":"前置詞句", "pronunciation_ja":"カタカナ", "meaning_ja":"意味", "note_ja":"メモ"}
        ))
    if grammar.get("conjugation"):
        blocks.append(html.H6("動詞変化：現在形"))
        blocks.append(render_key_value_table(
            grammar["conjugation"],
            ["person", "form", "pronunciation_ja", "ja"],
            {"person":"人称", "form":"形", "pronunciation_ja":"カタカナ", "ja":"意味"}
        ))
    if grammar.get("imperative"):
        blocks.append(html.H6("命令・依頼でよく使う形"))
        blocks.append(render_key_value_table(
            grammar["imperative"],
            ["label", "form", "pronunciation_ja", "ja"],
            {"label":"形", "form":"クロアチア語", "pronunciation_ja":"カタカナ", "ja":"意味"}
        ))
    if grammar.get("forms"):
        blocks.append(html.H6("語形の確認"))
        blocks.append(render_key_value_table(grammar["forms"], ["label", "form", "pronunciation_ja", "note"]))
    if not blocks:
        blocks.append(html.Div("この単語は、初級旅行表現では固定表現として扱います。変化表は必要に応じて後から追加できます。", className="muted"))
    return html.Div(blocks)


def render_vocab_item(item: Dict[str, Any]):
    meta = [pos_badge(item)]
    if item.get("gender"):
        meta.append(dbc.Badge(f"性: {item['gender']}", color="info", className="me-1"))
    if item.get("scene"):
        meta.append(dbc.Badge(item["scene"], color="light", text_color="dark", className="me-1"))

    examples = item.get("examples", [])
    example_rows = []
    for ex in examples:
        example_rows.append(html.Div([
            html.Div(ex.get("hr", ""), className="example-hr"),
            html.Div(ex.get("pronunciation_ja", ""), className="example-pronunciation"),
            html.Div(ex.get("ja", ""), className="example-ja"),
        ], className="example-block"))

    return dbc.Card(dbc.CardBody([
        html.Div([
            html.Div([
                html.Div(item.get("hr", ""), className="list-target-text"),
                html.Div(item.get("pronunciation_ja", ""), className="list-pronunciation"),
                html.Div(item.get("ja", ""), className="list-translation"),
            ]),
            html.Div(meta, className="badge-row"),
        ], className="list-card-head"),
        html.Details([
            html.Summary("例文・変化表を確認"),
            html.Div([
                html.H6("例文"),
                html.Div(example_rows or html.Div("例文は未登録です。", className="muted")),
                html.Hr(),
                render_inflection_block(item),
            ], className="details-box"),
        ], className="native-details"),
    ]), className="list-item-card")


def render_sentence_item(item: Dict[str, Any]):
    grammar = item.get("grammar", {})
    grammar_blocks = [
        html.H6(grammar.get("title", "文法解説")),
        html.P(grammar.get("explanation_ja", "文法解説は未登録です。")),
    ]
    for table in grammar.get("tables", []):
        grammar_blocks.append(html.H6(table.get("title_ja", "表")))
        headers = table.get("headers") or (list(table.get("rows", [{}])[0].keys()) if table.get("rows") else [])
        labels = table.get("header_labels", {})
        grammar_blocks.append(render_key_value_table(table.get("rows", []), headers, labels))
    if grammar.get("notes"):
        grammar_blocks.append(html.H6("補足"))
        grammar_blocks.append(html.Ul([html.Li(n) for n in grammar.get("notes", [])]))
    return dbc.Card(dbc.CardBody([
        html.Div(item.get("hr", ""), className="list-target-text"),
        html.Div(item.get("pronunciation_ja", ""), className="list-pronunciation"),
        html.Div(item.get("ja", ""), className="list-translation"),
        html.Details([
            html.Summary("単語・文法解説を確認"),
            html.Div([
                html.H6("単語ごとの意味"),
                render_tokens(item.get("tokens")),
                html.Hr(),
                html.Div(grammar_blocks),
            ], className="details-box"),
        ], className="native-details"),
    ]), className="list-item-card")


def render_paginated_list(title: str, subtitle: str, items: List[Dict[str, Any]], page_index: int, renderer):
    if not items:
        return dbc.Alert("該当する項目がありません。シーン・難易度・品詞を変更してください。", color="warning")
    total_pages = max(1, math.ceil(len(items) / ITEMS_PER_PAGE))
    page = int(page_index or 0) % total_pages
    start = page * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE
    visible_items = items[start:end]
    return dbc.Card(dbc.CardBody([
        html.Div([
            card_header(title, subtitle),
        ], className="list-title-row"),
        html.Div(f"{len(items)}件中 {start + 1}〜{min(end, len(items))}件を表示 / ページ {page + 1}/{total_pages}", className="muted mb-3"),
        html.Div([renderer(item) for item in visible_items], className="list-stack scrollable-list"),
    ]), className="main-card")


def get_quiz_pool(scenes, level):
    return filter_by_scene_and_level(DATA["sentences"], scenes, level)


def make_choices(correct: str, direction: str, pool: List[Dict[str, Any]]):
    field = "hr" if direction == "ja_to_hr" else "ja"
    candidates = [x.get(field, "") for x in pool if x.get(field, "") != correct]
    choices = random.sample(candidates, min(3, len(candidates))) + [correct]
    random.shuffle(choices)
    return choices


def render_multiple_choice(item: Dict[str, Any], direction: str, pool: List[Dict[str, Any]]):
    prompt = item["ja"] if direction == "ja_to_hr" else item["hr"]
    correct = item["hr"] if direction == "ja_to_hr" else item["ja"]
    choices = make_choices(correct, direction, pool)
    return dbc.Card(dbc.CardBody([
        card_header("四択クイズ", "正しい訳を選んでください。"),
        html.Div(prompt, className="quiz-prompt"),
        dcc.RadioItems(
            id="mc-answer",
            options=[{"label": c, "value": c} for c in choices],
            className="choice-list",
            inputClassName="me-2",
            labelClassName="choice-label",
        ),
        dbc.Button("回答する", id="check-mc", color="primary", className="mt-3"),
        html.Div(id="mc-result", className="result-box"),
    ]), className="main-card")


def render_input_quiz(item: Dict[str, Any], direction: str):
    prompt = item["ja"] if direction == "ja_to_hr" else item["hr"]
    answer_label = "クロアチア語で入力" if direction == "ja_to_hr" else "日本語で入力"
    return dbc.Card(dbc.CardBody([
        card_header("入力クイズ", "句読点・大文字小文字はゆるく判定します。"),
        html.Div(prompt, className="quiz-prompt"),
        dbc.Label(answer_label),
        dbc.Input(id="input-answer", type="text", placeholder="ここに入力", debounce=False),
        dbc.Checklist(
            options=[{"label":"クロアチア語のč/ć/š/ž/đを厳密に判定する", "value":"strict"}],
            value=[], id="strict-diacritics", switch=True, className="mt-2"
        ),
        dbc.Button("回答する", id="check-input", color="primary", className="mt-3 me-2"),
        dbc.Button("発音ヒント", id="toggle-input-hint", color="outline-secondary", className="mt-3", size="sm"),
        html.Div(id="input-hint-box"),
        html.Div(id="input-result", className="result-box"),
    ]), className="main-card")


def render_dialogue_card(item: Dict[str, Any]):
    lines = []
    translations = []
    for line in item.get("dialogue", []):
        lines.append(html.Div([
            html.Span(f"{line.get('speaker', '')}: ", className="speaker"),
            html.Span(line.get("hr", ""), className="dialogue-hr"),
            html.Div(line.get("pronunciation_ja", ""), className="dialogue-pronunciation"),
        ], className="dialogue-line"))
        translations.append(html.Div([
            html.Span(f"{line.get('speaker', '')}: ", className="speaker"),
            html.Span(line.get("ja", "")),
        ], className="translation-line"))

    questions = []
    for q in item.get("questions", []):
        if q.get("type") == "multiple_choice":
            questions.append(html.Div([
                html.H5(q.get("question_ja", "")),
                dcc.RadioItems(
                    id={"type":"dialogue-mc", "index": q["id"]},
                    options=[{"label": c, "value": c} for c in q.get("choices_ja", [])],
                    className="choice-list",
                    inputClassName="me-2",
                    labelClassName="choice-label",
                ),
                dbc.Button("回答する", id={"type":"dialogue-mc-button", "index": q["id"]}, color="primary", size="sm", className="mt-2"),
                html.Div(id={"type":"dialogue-mc-result", "index": q["id"]}, className="result-box"),
            ], className="question-block"))
        elif q.get("type") == "input":
            questions.append(html.Div([
                html.H5(q.get("question_ja", "")),
                dbc.Input(id={"type":"dialogue-input", "index": q["id"]}, placeholder="ここに入力"),
                dbc.Button("回答する", id={"type":"dialogue-input-button", "index": q["id"]}, color="primary", size="sm", className="mt-2"),
                html.Div(id={"type":"dialogue-input-result", "index": q["id"]}, className="result-box"),
            ], className="question-block"))

    grammar_notes = [html.Div([html.H5(n.get("title_ja", "")), html.P(n.get("explanation_ja", ""))]) for n in item.get("grammar_notes", [])]

    return dbc.Card(dbc.CardBody([
        card_header(short_ja_title(item.get("title_ja", "対話読解")), None),
        html.Div(lines, className="dialogue-box"),
        html.Details([
            html.Summary("日本語訳を表示"),
            html.Div(translations, className="details-box"),
        ], className="native-details"),
        html.Details([
            html.Summary("単語解説を表示"),
            html.Div([
                html.H5("この読解に出てきた語句"),
                render_dialogue_vocab_notes(item.get("vocabulary_notes")),
                html.Hr() if item.get("seafood_table") else None,
                html.H5("魚介類の名前") if item.get("seafood_table") else None,
                render_seafood_table(item.get("seafood_table")),
            ], className="details-box"),
        ], className="native-details"),
        html.Details([
            html.Summary("文法メモを表示"),
            html.Div(grammar_notes, className="details-box"),
        ], className="native-details"),
        html.Hr(),
        html.H4("読解問題"),
        html.Div(questions),
    ]), className="main-card scrollable-card")


def render_reference(ref_id: str):
    ref = DATA["references"].get(ref_id) or next(iter(DATA["references"].values()))
    section_cards = []
    for section in ref.get("sections", []):
        rows = [html.Tr([html.Th("日本語/値"), html.Th("クロアチア語"), html.Th("カタカナ"), html.Th("メモ")])]
        for item in section.get("items", []):
            rows.append(html.Tr([
                html.Td(item.get("ja", item.get("value", ""))),
                html.Td(item.get("hr", "")),
                html.Td(item.get("pronunciation_ja", "")),
                html.Td(item.get("note_ja", "")),
            ]))
        children = [
            html.H4(section.get("title_ja", "")),
            html.P(section.get("note_ja", ""), className="muted") if section.get("note_ja") else None,
            dbc.Table(rows, bordered=True, hover=True, responsive=True, className="reference-table"),
            section_examples(section.get("examples")),
        ]
        section_cards.append(html.Div(children, className="reference-section"))
    return dbc.Card(dbc.CardBody([
        card_header(f"参考：{ref.get('title_ja', '')}", None),
        html.Div(section_cards, className="reference-scroll")
    ]), className="main-card")


app.layout = dbc.Container([
    dcc.Store(id="current-index", data=0),
    dcc.Store(id="current-item", data=None),
    dcc.Store(id="input-hint-visible", data=False),
    html.Div([
        html.H1("クロアチア語旅行", className="app-title"),
        html.P("夏の旅行で使う初級表現", className="app-subtitle"),
    ], className="header"),
    dbc.Row([
        dbc.Col([
            dbc.Card(dbc.CardBody([
                html.H4("設定", className="settings-title"),
                dbc.Accordion([
                    dbc.AccordionItem([
                        dcc.RadioItems(id="mode", options=MODES, value="vocab", className="radio-list", inputClassName="me-2"),
                    ], title="モード", item_id="mode-panel"),
                    dbc.AccordionItem([
                        dcc.Checklist(id="scene-checklist", options=SCENES, value=[s["value"] for s in SCENES], className="check-list", inputClassName="me-2"),
                    ], title="シーン", item_id="scene-panel"),
                    dbc.AccordionItem([
                        html.Div(id="pos-filter-wrap", children=[
                            dcc.Checklist(id="pos-filter", options=POS_OPTIONS, value=[o["value"] for o in POS_OPTIONS], className="check-list", inputClassName="me-2"),
                        ]),
                    ], title="単語の役割", item_id="pos-panel"),
                    dbc.AccordionItem([
                        dcc.Dropdown(id="level", options=[{"label":f"Level {i}まで", "value":i} for i in [1,2,3]], value=2, clearable=False),
                    ], title="難易度", item_id="level-panel"),
                    dbc.AccordionItem([
                        dcc.RadioItems(id="direction", options=DIRECTIONS, value="ja_to_hr", className="radio-list", inputClassName="me-2"),
                    ], title="翻訳方向", item_id="direction-panel"),
                    dbc.AccordionItem([
                        html.Div(id="reference-selector-wrap", children=[
                            dcc.Dropdown(id="reference-select", options=REFERENCE_OPTIONS, value="numbers", clearable=False),
                        ]),
                        html.Div(id="dialogue-selector-wrap", children=[
                            dcc.Dropdown(id="dialogue-select", options=[], value=None, clearable=False),
                        ]),
                    ], title="詳細選択", item_id="detail-panel"),
                ], start_collapsed=True, always_open=True, className="settings-accordion"),
                dbc.Button("次の問題 / 次の対話", id="next-button", color="success", className="mt-3 w-100"),
            ]), className="sidebar")
        ], md=4, lg=3),
        dbc.Col([
            html.Div([
                dbc.Button("前へ", id="page-prev", color="outline-primary", size="sm", className="me-2"),
                dbc.Button("次へ", id="page-next", color="primary", size="sm"),
            ], id="page-controls-wrap", className="page-controls-top"),
            html.Div(id="main-content"),
        ], md=8, lg=9),
    ])
], fluid=True, className="page")


@app.callback(
    Output("reference-selector-wrap", "style"),
    Output("pos-filter-wrap", "style"),
    Output("dialogue-selector-wrap", "style"),
    Output("next-button", "style"),
    Output("page-controls-wrap", "style"),
    Input("mode", "value")
)
def show_mode_specific_controls(mode):
    return (
        {"display":"block"} if mode == "reference" else {"display":"none"},
        {"display":"block"} if mode == "vocab" else {"display":"none"},
        {"display":"block"} if mode == "dialogue" else {"display":"none"},
        {"display":"block"} if mode in ["multiple_choice", "input_quiz", "dialogue"] else {"display":"none"},
        {"display":"flex"} if mode in ["vocab", "sentences"] else {"display":"none"},
    )


@app.callback(
    Output("current-index", "data"),
    Input("next-button", "n_clicks"),
    Input("page-next", "n_clicks"),
    Input("page-prev", "n_clicks"),
    State("current-index", "data"),
    prevent_initial_call=False,
)
def change_index(next_clicks, page_next_clicks, page_prev_clicks, current):
    if not dash.callback_context.triggered:
        return 0
    triggered = dash.callback_context.triggered_id
    if triggered in ["next-button", "page-next"]:
        return int(current or 0) + 1
    if triggered == "page-prev":
        return int(current or 0) - 1
    return int(current or 0)


@app.callback(
    Output("dialogue-select", "options"),
    Output("dialogue-select", "value"),
    Input("scene-checklist", "value"),
    Input("level", "value"),
    State("dialogue-select", "value"),
)
def update_dialogue_selector(scenes, level, current_value):
    pool = filter_by_scene_and_level(DATA["dialogues"], scenes, level)
    options = [{"label": short_ja_title(d.get("title_ja", "")), "value": d.get("id")} for d in pool]
    values = {o["value"] for o in options}
    value = current_value if current_value in values else (options[0]["value"] if options else None)
    return options, value


@app.callback(
    Output("main-content", "children"),
    Output("current-item", "data"),
    Output("input-hint-visible", "data"),
    Input("mode", "value"),
    Input("scene-checklist", "value"),
    Input("pos-filter", "value"),
    Input("level", "value"),
    Input("direction", "value"),
    Input("reference-select", "value"),
    Input("dialogue-select", "value"),
    Input("current-index", "data"),
)
def update_main(mode, scenes, pos_filter, level, direction, reference_id, dialogue_id, idx):
    idx = int(idx or 0)
    if mode == "reference":
        return render_reference(reference_id), None, False

    if mode == "vocab":
        pool = filter_by_scene_and_level(DATA["vocabulary"], scenes, level)
        pos_filter = set(pos_filter or [])
        if pos_filter:
            pool = [x for x in pool if x.get("part_of_speech", "other") in pos_filter]
        return render_paginated_list(
            "単語学習",
            "単語・カタカナ・意味を一覧で確認します。各カードを開くと例文と変化表を確認できます。",
            pool,
            idx,
            render_vocab_item,
        ), None, False

    if mode == "sentences":
        pool = get_quiz_pool(scenes, level)
        return render_paginated_list(
            "例文学習",
            "シーン別の例文を一覧で確認します。各カードを開くと単語分解と文法解説を確認できます。",
            pool,
            idx,
            render_sentence_item,
        ), None, False

    if mode in ["multiple_choice", "input_quiz"]:
        pool = get_quiz_pool(scenes, level)
        if not pool:
            return dbc.Alert("該当する例文がありません。シーンまたは難易度を変更してください。", color="warning"), None, False
        item = pool[idx % len(pool)]
        if mode == "multiple_choice":
            return render_multiple_choice(item, direction, pool), item, False
        return render_input_quiz(item, direction), item, False

    if mode == "dialogue":
        pool = filter_by_scene_and_level(DATA["dialogues"], scenes, level)
        if not pool:
            return dbc.Alert("該当する対話文がありません。シーンまたは難易度を変更してください。", color="warning"), None, False
        item = next((d for d in pool if d.get("id") == dialogue_id), None) or pool[idx % len(pool)]
        return render_dialogue_card(item), item, False

    return dbc.Alert("未対応のモードです。", color="danger"), None, False


@app.callback(
    Output("input-hint-visible", "data", allow_duplicate=True),
    Input("toggle-input-hint", "n_clicks"),
    State("input-hint-visible", "data"),
    prevent_initial_call=True,
)
def toggle_input_hint(n, visible):
    return not bool(visible)


@app.callback(
    Output("input-hint-box", "children"),
    Input("input-hint-visible", "data"),
    State("current-item", "data"),
    prevent_initial_call=True,
)
def render_input_hint(visible, item):
    if not visible or not item:
        return ""
    return html.Div(item.get("pronunciation_ja", ""), className="pronunciation collapse-box")


@app.callback(
    Output("mc-result", "children"),
    Input("check-mc", "n_clicks"),
    State("mc-answer", "value"),
    State("current-item", "data"),
    State("direction", "value"),
    prevent_initial_call=True,
)
def check_mc(n, selected, item, direction):
    if not item or selected is None:
        return dbc.Alert("選択肢を選んでください。", color="warning")
    correct = item["hr"] if direction == "ja_to_hr" else item["ja"]
    pronunciation = item.get("pronunciation_ja", "")
    confirmation = html.Div([
        html.Div("正解後確認", className="result-title"),
        html.Div(item.get("hr", ""), className="result-answer"),
        html.Div(pronunciation, className="result-pronunciation"),
        html.Div(item.get("ja", ""), className="result-ja"),
    ], className="answer-confirm-box")
    if selected == correct:
        return html.Div([dbc.Alert("正解です！", color="success"), confirmation])
    return html.Div([dbc.Alert(["不正解です。正解：", html.Strong(correct)], color="danger"), confirmation])


@app.callback(
    Output("input-result", "children"),
    Input("check-input", "n_clicks"),
    State("input-answer", "value"),
    State("current-item", "data"),
    State("direction", "value"),
    State("strict-diacritics", "value"),
    prevent_initial_call=True,
)
def check_input(n, answer, item, direction, strict_value):
    if not item or not answer:
        return dbc.Alert("回答を入力してください。", color="warning")
    strict = "strict" in (strict_value or [])
    accepted = item.get("accepted_answers_hr", [item.get("hr", "")]) if direction == "ja_to_hr" else item.get("accepted_answers_ja", [item.get("ja", "")])
    correct = item.get("hr", "") if direction == "ja_to_hr" else item.get("ja", "")
    confirmation = html.Div([
        html.Div("正解後確認", className="result-title"),
        html.Div(item.get("hr", ""), className="result-answer"),
        html.Div(item.get("pronunciation_ja", ""), className="result-pronunciation"),
        html.Div(item.get("ja", ""), className="result-ja"),
    ], className="answer-confirm-box")
    if check_answer(answer, accepted, strict_diacritics=strict):
        return html.Div([dbc.Alert("正解です！", color="success"), confirmation])
    return html.Div([dbc.Alert(["不正解です。正解例：", html.Strong(correct)], color="danger"), confirmation])


@app.callback(
    Output({"type":"dialogue-mc-result", "index": dash.MATCH}, "children"),
    Input({"type":"dialogue-mc-button", "index": dash.MATCH}, "n_clicks"),
    State({"type":"dialogue-mc", "index": dash.MATCH}, "value"),
    State("current-item", "data"),
    prevent_initial_call=True,
)
def check_dialogue_mc(n, selected, item):
    triggered = dash.callback_context.triggered_id
    qid = triggered["index"] if isinstance(triggered, dict) else None
    question = next((q for q in item.get("questions", []) if q.get("id") == qid), None)
    if not selected:
        return dbc.Alert("選択肢を選んでください。", color="warning")
    if question and selected == question.get("answer"):
        return dbc.Alert("正解です！", color="success")
    return dbc.Alert(["不正解です。正解：", html.Strong(question.get("answer", ""))], color="danger")


@app.callback(
    Output({"type":"dialogue-input-result", "index": dash.MATCH}, "children"),
    Input({"type":"dialogue-input-button", "index": dash.MATCH}, "n_clicks"),
    State({"type":"dialogue-input", "index": dash.MATCH}, "value"),
    State("current-item", "data"),
    prevent_initial_call=True,
)
def check_dialogue_input(n, answer, item):
    triggered = dash.callback_context.triggered_id
    qid = triggered["index"] if isinstance(triggered, dict) else None
    question = next((q for q in item.get("questions", []) if q.get("id") == qid), None)
    if not answer:
        return dbc.Alert("回答を入力してください。", color="warning")
    accepted = question.get("accepted_answers_hr", [question.get("answer_hr", "")]) if question else []
    correct = question.get("answer_hr", "") if question else ""
    if check_answer(answer, accepted, strict_diacritics=False):
        return dbc.Alert("正解です！", color="success")
    return dbc.Alert(["不正解です。正解例：", html.Strong(correct)], color="danger")


if __name__ == "__main__":
    app.run_server(debug=True)

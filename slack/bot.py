import os

import requests
from fastapi import FastAPI, Request
from slack_bolt import Ack, App
from slack_bolt.adapter.fastapi import SlackRequestHandler

# Slack Appの初期化
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.shortcut("search_papers")
def open_modal(ack: Ack, body: dict, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Research Paper Search"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "keyword_block",
                    "label": {"type": "plain_text", "text": "Keyword"},
                    "element": {"type": "plain_text_input", "action_id": "keyword"},
                },
                {
                    "type": "input",
                    "block_id": "num_paper_block",
                    "label": {"type": "plain_text", "text": "Number of Papers"},
                    "element": {"type": "plain_text_input", "action_id": "num_paper", "initial_value": "1"},
                },
                {
                    "type": "input",
                    "block_id": "openai_model",
                    "label": {"type": "plain_text", "text": "OpenAI Model"},
                    "element": {
                        "type": "static_select",
                        "action_id": "openai_model",
                        "initial_option": {
                            "text": {"type": "plain_text", "text": "gpt-3.5-turbo"},
                            "value": "gpt-3.5-turbo",
                        },
                        "options": [
                            {"text": {"type": "plain_text", "text": "gpt-3.5-turbo"}, "value": "gpt-3.5-turbo"},
                            {"text": {"type": "plain_text", "text": "gpt-4"}, "value": "gpt-4"},
                            {"text": {"type": "plain_text", "text": "None"}, "value": "None"},
                        ],
                    },
                },
            ],
            "submit": {"type": "plain_text", "text": "Submit"},
        },
    )


def get_result(endpoint: str, params: dict):
    if params["openai_model"] == "None":
        url = f"{endpoint}/paper/"
        del params["openai_model"]
        return requests.get(url=url, params=params).json()
    else:
        url = f"{endpoint}/formatted_summary/"
        return requests.get(url=url, params=params).json()


# モーダルからのデータ受信と処理
@app.view("view_1")
def handle_submission(ack: Ack, body: dict, client):
    ack()
    # ユーザーが入力した情報を取得
    params = {
        "keyword": body["view"]["state"]["values"]["keyword_block"]["keyword"]["value"],
        "items_per_page": body["view"]["state"]["values"]["num_paper_block"]["num_paper"]["value"],
        "openai_model": body["view"]["state"]["values"]["openai_model"]["openai_model"]["selected_option"]["value"],
        "page": 1,
    }

    endpoint = os.getenv("PWC_NIGIRI_API_ENDPOINT")
    result = get_result(endpoint, params)

    # 結果をユーザーに送信
    user_id = body["user"]["id"]
    for text in result:
        client.chat_postMessage(channel=user_id, text=str(text))


fastapi_app = FastAPI()
handler = SlackRequestHandler(app)


# FastAPIのルートにslack_boltのリクエストハンドラを追加
@fastapi_app.post("/slack/events")
async def endpoint(req: Request):
    return await handler.handle(req)

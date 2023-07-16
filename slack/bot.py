import os

from fastapi import FastAPI, Request
from slack_bolt import Ack, App
from slack_bolt.adapter.fastapi import SlackRequestHandler

# Slack Appの初期化
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)


@app.shortcut("research_paper_search")
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
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "num_paper",
                        "initial_value": "1",
                    },
                },
                {
                    "type": "input",
                    "block_id": "openai_model",
                    "label": {"type": "plain_text", "text": "OpenAI Model"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "openai_model",
                        "initial_value": "gpt-3.5-turbo",
                    },
                },
            ],
            "submit": {"type": "plain_text", "text": "Submit"},
        },
    )


# モーダルからのデータ受信と処理
@app.view("view_1")
def handle_submission(ack: Ack, body: dict, client):
    ack()
    # ユーザーが入力した情報を取得
    keyword = body["view"]["state"]["values"]["keyword_block"]["keyword"]["value"]
    num_paper = body["view"]["state"]["values"]["num_paper_block"]["num_paper"]["value"]

    # APIにリクエストを送り、結果を取得
    # ここではサンプルとして静的なテキストを設定
    result = f"Keyword: {keyword}, Number of papers: {num_paper}"

    # 結果をユーザーに送信
    user_id = body["user"]["id"]
    client.chat_postMessage(channel=user_id, text=result)


fastapi_app = FastAPI()
handler = SlackRequestHandler(app)


# FastAPIのルートにslack_boltのリクエストハンドラを追加
@fastapi_app.post("/slack/events")
async def endpoint(req: Request):
    return await handler.handle(req)

# paperswithcode-nigiri
論文翻訳 & 要約をする Slack Bots

## API
- paperswithcode api で任意の keyword を検索し、任意の数取得します。取得した論文それぞのタイトルとアブストラクトを OpenAI api を用いて日本語に翻訳し、要約を追加します。
- FastAPI を使っています。

### Cloud Run にデプロイする
1. Project の設定 : gcloud コマンドが使用できるようになっている状態
    ```
    PROJECT_ID={作成したプロジェクトのID}
    gcloud config set project ${PROJECT_ID}
    gcloud config set run/region asia-northeast1
    ```
2. container image
    ```
    # api dir に移動する
    cd ./paperswithcode-nigiri/api
    docker buildx build --platform linux/amd64 -t asia.gcr.io/${PROJECT_ID}/fastapi-image:v1 .
    ```
    - M1M2チップのMacを使っている場合、上記のように `--platform linux/amd64` 必要

3. google cloud の container registry に push
    ```
    docker push asia.gcr.io/${PROJECT_ID}/fastapi-image:v1
    ```

4. google cloud console から cloud run にデプロイする
    - 環境変数の設定をする (`TEMPERATURE` など)
    - `OPENAI_API_KEY` などの secret は `Secret Manager` に登録し、環境変数などで利用するようにする (非推奨?)
    - 公開範囲は限定しない
    - URLの取得 (`{URL}/paper/?keyword=resnet` などで疎通確認する)

## Slack
- slack bot を作成する。bot を呼び出した際にモーダル表示がされ、そこから `keyword` などを入れてサブミットすると、APIにリクエストを送り、論文検索結果をユーザーに表示する。

### Cloud Run にデプロイする
- api のデプロイ時と同様だが、image の名前を適当に変える。
- 環境変数として API のURLを指定する必要がある。
- secret として `SLACK_BOT_TOKEN` と `SLACK_SIGINGIN_SECRET` を登録する
- URL の取得 → `Request URL` に使用する

### Slack app
1. slack app を作成する
2. slack app の設定を行う
    - `Add features and functionality` : **Bots** 
    - `Scopes` : **chat:write** → Revoke Tokens
    - `OAuth Tokens for Your Workspace` : **Install to Workspace** のち `SLACK_BOT_TOKEN` (`Bot User OAuth Token`) を取得する
    - **`Basic Information`** : `SLACK_SIGNING_TOKEN` (`Signing Secret`) を取得する
3. **`Interactivity & Shortcuts`**` の設定
    - `Request URL`: デプロイ時に取得したURLを入力する。今回は `{URL}/slack/events` を指定する。
        ```
        @fastapi_app.post("/slack/events")
        async def endpoint(req: Request):
        ```
    - `Create a shortcut` : name には `search_papers` を指定。 
        ```
        @app.shortcut("search_papers")
        def open_modal(ack: Ack, body: dict, client):
        ```


## その他
- cloud run と slack app に触ってみたくて作ってみました。
- api 部分と slack 部分は別に分けなくもいいですが、今回は分けてみました。
- openai の api は別途利用登録と利用料金がかかります。
- 全部ローカルで済ませたい (cloud run にデプロイしたくない) 場合やローカルでの開発時は `ngrok` が便利です

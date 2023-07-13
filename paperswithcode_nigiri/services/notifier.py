import slackweb
from retry import retry


@retry(tries=3, delay=1)
def notice_slack(webhook_url: str, message: str) -> None:
    slack = slackweb.Slack(url=webhook_url)
    slack.notify(text=message)

import datetime

import slackweb
from retry import retry


class SlackNotifier:
    def __init__(self, webhook_url: str) -> None:
        """
        SlackNotifierクラスのコンストラクタです。

        Args:
            webhook_url (str): SlackのWebhook URL
        """
        self.slack = slackweb.Slack(url=webhook_url)

    def _is_mention_time(self) -> bool:
        """
        現在の時刻がメンションの送信時間帯かどうかを判定します。

        Returns:
            bool: メンションの送信時間帯であればFalse、そうでなければTrue
        """
        hour = datetime.datetime.now().hour
        if hour >= 15 and hour <= 21:
            return False
        else:
            return True

    @retry(tries=3, delay=1)
    def notify(
        self,
        message: str,
        mention_targets: None | list[str] = None,
        force_mention: bool = False,
    ) -> None:
        """
        Slackに通知を送信します。

        Args:
            message (str): 通知メッセージ
            mention_targets (None | list[str], optional): メンション対象のユーザー名のリスト。デフォルトはNone。
            force_mention (bool, optional): 強制的にメンションを付けるかどうかのフラグ。デフォルトはFalse。
        """
        if force_mention or ((mention_targets is not None) and self._is_mention_time()):
            mention = "<@" + " @".join(["a", "b", "c"]) + "> "  # TODO: テスト
            message = mention + message

        self.slack.notify(text=message)

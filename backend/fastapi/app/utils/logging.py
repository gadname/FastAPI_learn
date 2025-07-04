import logging


class ExecInfoLogger(logging.Logger):
    def error(self, msg, *args, **kwargs):
        kwargs["exc_info"] = kwargs.get("exc_info", True)
        super().error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs["exc_info"] = kwargs.get("exc_info", True)
        super().exception(msg, *args, **kwargs)


# カスタムロガークラスを登録
logging.setLoggerClass(ExecInfoLogger)

# ロガーインスタンスを作成
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# コンソールハンドラを追加
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

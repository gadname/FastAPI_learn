import logging


class ExecInfoLogger(logging.Logger):
    def error(self, msg, *args, **kwargs):
        kwargs["exc_info"] = kwargs.get("exc_info", True)
        super().error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        kwargs["exc_info"] = kwargs.get("exc_info", True)
        super().exception(msg, *args, **kwargs)

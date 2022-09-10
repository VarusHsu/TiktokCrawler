from PyQt6.QtCore import QObject

import feishu


class Logger:
    signals_sender: QObject
    lark_sender: feishu.Feishu

    def __init__(self, signals_sender: QObject, lark_sender: feishu.Feishu):
        self.lark_sender = lark_sender
        self.signals_sender = signals_sender

    def LogMessage(self, message_type: str, message_text: str, notice_email: str = ""):
        message: str = f"[{message_type.upper()}] {message_text}"
        self.lark_sender.send_lark(message, notice_email)
        self.signals_sender.log_signal.emit(message)


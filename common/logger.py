from threading import Thread

from PyQt6.QtCore import QObject

from common import feishu


class Logger:
    signals_sender: QObject
    lark_sender: feishu.Feishu

    def __init__(self, signals_sender: 'QObject| None', lark_sender: feishu.Feishu):
        self.lark_sender = lark_sender
        self.signals_sender = signals_sender

    def log_message(self, message_type: str, message_text: str, notice_email: str = ""):
        message: str = f"[{message_type.upper()}] {message_text}"

        def run(send_message: str, email: str):
            self.lark_sender.send_lark(send_message, email)
        send_lark_thread: Thread = Thread(target=run, args=(message, notice_email))
        send_lark_thread.start()
        message = self.__remove_illegal_byte(message)
        if self.signals_sender is not None:
            self.signals_sender.log_signal.emit(message)

    @staticmethod
    def __remove_illegal_byte(text: str) -> str:
        res: str = ""
        for byte in text:
            if byte.isascii():
                res = res + byte
        return res


import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton

from feishu import Feishu
from logger import Logger
from reporter import Reporter
from requester import Requester
from signals import UpdateUISignals, AdjustConfigSignals
from xlsx_worker import XlsxWorker
from generate_path import default_path


class PlayCountCrawler(QObject):

    # module
    feishu: Feishu
    reporter: Reporter
    requester: Requester
    logger: Logger
    xlsx_reader: XlsxWorker
    xlsx_writer: XlsxWorker

    # ui_widget
    app: QApplication
    windows: QWidget
    log_box: QListWidget
    crawl_button: QPushButton
    import_button: QPushButton
    config_button: QPushButton

    # signals
    update_ui_signals: UpdateUISignals
    adjust_config_signals: AdjustConfigSignals

    # status
    output_path = default_path
    input_file_name = ''

    def __init__(self):
        super().__init__()

        self.update_ui_signals = UpdateUISignals()
        self.adjust_config_signals = AdjustConfigSignals()
        self.feishu = Feishu()
        self.logger = Logger(lark_sender=self.feishu, signals_sender=self.update_ui_signals)
        self.requester = Requester(logger=self.logger)

    def render(self):
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.resize(750, 421)
        self.windows.setWindowTitle("Jojoy tiktok play information")
        self.windows.setFixedSize(750, 421)

        self.log_box = QListWidget(self.windows)
        self.log_box.move(20, 20)
        self.log_box.resize(710, 361)
        self.log_box.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.crawl_button = QPushButton(self.windows)
        self.crawl_button.setText("Run")
        self.crawl_button.move(20, 385)

        self.import_button = QPushButton(self.windows)
        self.import_button.setText("Open")
        self.import_button.move(330, 385)

        self.config_button = QPushButton(self.windows)
        self.config_button.setText("Setting")
        self.config_button.move(660, 385)




        self.windows.show()
        sys.exit(self.app.exec())
        pass

    def handle_crawl_button_clicked(self):
        pass

    def handle_import_button_clicked(self):
        pass

    def handle_config_button_clicked(self):
        pass


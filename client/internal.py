import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QFileDialog

from common.feishu import Feishu
from generate.generate_path import default_path
from common.logger import Logger
from common.reporter import Reporter
from common.requester import Requester
from common.signals import UpdateUISignals, AdjustConfigSignals
from common.enums import ListType


class DownloadWindows(QObject):

    windows: QWidget
    log_box: QListWidget
    items: []

    list_type: ListType
    requester: Requester

    def __init__(self, list_type: ListType, requester: Requester):
        super().__init__()
        self.list_type = list_type
        self.requester = requester

    def render(self):
        self.windows = QWidget()
        if self.list_type == ListType.ByTime:
            self.windows.setWindowTitle("Download By Time")
        else:
            self.windows.setWindowTitle("Download By Increase")
        self.windows.resize(500, 314)
        self.windows.setFixedSize(500, 314)

        pass


class PlayCountClient(QObject):
    feishu: Feishu
    reporter: Reporter
    requester: Requester
    logger: Logger

    # ui_widget
    app: QApplication
    windows: QWidget
    log_box: QListWidget
    get_history_button: QPushButton
    upload_button: QPushButton
    download_by_time_button: QPushButton
    download_by_increase_button: QPushButton
    setting_button: QPushButton
    import_file_dialog: QFileDialog
    output_path_file_dialog: QFileDialog
    download_windows: DownloadWindows

    # signals
    update_ui_signals: UpdateUISignals
    adjust_config_signals: AdjustConfigSignals

    # status
    task_list = []
    remove_duplication_author = []
    remove_duplication_page = []
    hashtag_str = ''
    output_path = default_path
    input_file_name = ''
    notice_email = ''
    ms_token = 'g8vXKy2fjhjd7xrrPcCU7Wfop7isL5KAuyjofBp061Mtaxm_fA5vZ_lAlj46mvE_NnR7x-m-022QnOLdb6Em6HbYv1qm-ek2LXKHh6aTtnLpk_Ke8h7MUTkvWAUZX0cQ1JhrowY='

    def __init__(self):
        super().__init__()

        self.update_ui_signals = UpdateUISignals()
        self.adjust_config_signals = AdjustConfigSignals()

        self.feishu = Feishu()
        self.logger = Logger(lark_sender=self.feishu, signals_sender=self.update_ui_signals)
        self.requester = Requester(logger=self.logger)
        self.reporter = Reporter()

    def render(self):
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.resize(750, 421)
        self.windows.setWindowTitle("Played Count Client")
        self.windows.setFixedSize(750, 421)

        self.upload_button = QPushButton(self.windows)
        self.upload_button.setText("Update Data Source")
        self.upload_button.setFixedWidth(150)
        self.upload_button.move(20, 385)

        self.download_by_time_button = QPushButton(self.windows)
        self.download_by_time_button.setText("Download By Time")
        self.download_by_time_button.setFixedWidth(150)
        self.download_by_time_button.move(210, 385)
        self.download_by_time_button.clicked.connect(self.handle_download_by_time_button_click)

        self.download_by_increase_button = QPushButton(self.windows)
        self.download_by_increase_button.setText("Download By Increase")
        self.download_by_increase_button.setFixedWidth(150)
        self.download_by_increase_button.move(390, 385)
        self.download_by_increase_button.clicked.connect(self.handle_download_by_increase_button_click)

        self.setting_button = QPushButton(self.windows)
        self.setting_button.setFixedWidth(150)
        self.setting_button.setText("Setting")
        self.setting_button.move(580, 385)

        self.log_box = QListWidget(self.windows)
        self.log_box.move(20, 20)
        self.log_box.resize(710, 361)
        self.log_box.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.windows.show()
        sys.exit(self.app.exec())
        pass

    def handle_download_by_time_button_click(self):
        self.download_windows = DownloadWindows(ListType.ByTime, self.requester)
        self.download_windows.render()

    pass

    def handle_download_by_increase_button_click(self):
        self.download_windows = DownloadWindows(ListType.ByIncrease, self.requester)
        self.download_windows.render()

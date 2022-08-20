import sys
from threading import Thread

import openpyxl
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QPushButton, QProgressBar, QListWidget, QWidget, QFileDialog
from PyQt6 import QtCore
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import openpyxl


class UpdateUISignals(QObject):
    log_signal = pyqtSignal(str, str)
    progress_bar_update_signal = pyqtSignal(int)


class VideoCrawler(QObject):

    app: QApplication
    windows: QWidget
    crawl_button: QPushButton
    import_button: QPushButton
    progress_bar: QProgressBar
    log_box: QListWidget

    window_width: int = 500
    window_height: int = 314
    button_width: int = 80
    button_height: int = 20
    edge_distance: int = 20

    ms_token = "g8vXKy2fjhjd7xrrPcCU7Wfop7isL5KAuyjofBp061Mtaxm_fA5vZ_lAlj46mvE_NnR7x-m-022QnOLdb6Em6HbYv1qm-ek2LXKHh6aTtnLpk_Ke8h7MUTkvWAUZX0cQ1JhrowY="

    file: str = ""
    task: dict = {}
    task_list: []

    update_ui_signals: UpdateUISignals

    def __init__(self):
        super().__init__()
        self.update_ui_signals = UpdateUISignals()
        self.update_ui_signals.progress_bar_update_signal.connect(self.handle_update_progress_bar_signal)
        self.update_ui_signals.log_signal.connect(self.handle_log_signal)

    def render(self):
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.resize(self.window_width, self.window_height)
        self.windows.setWindowTitle("短视频播放量爬虫（0.0）")
        self.windows.setFixedSize(self.windows.width(), self.windows.height())

        self.log_box = QListWidget(self.windows)
        self.log_box.move(self.edge_distance, self.edge_distance)
        self.log_box.resize(self.window_width - 2 * self.edge_distance, self.window_height - self.button_height - 3 * self.edge_distance)
        self.log_box.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.crawl_button = QPushButton(self.windows)
        self.crawl_button.setText("开始爬取")
        self.crawl_button.move(int(self.window_width / 3 * 2 - self.button_width / 2), int(self.window_height - self.edge_distance - self.button_height))
        self.crawl_button.clicked.connect(self.handle_crawl_button_click)

        self.import_button = QPushButton(self.windows)
        self.import_button.setText("导入表格")
        self.import_button.move(int(self.window_width / 3 * 1 - self.button_width / 2), int(self.window_height - self.edge_distance - self.button_height))
        self.import_button.clicked.connect(self.handle_import_button_click)

        self.progress_bar = QProgressBar(self.windows)
        self.progress_bar.resize(self.window_width - 2 * self.edge_distance, 15)
        self.progress_bar.move(self.edge_distance, 3)

        self.windows.show()
        sys.exit(self.app.exec())
        pass

    def handle_crawl_button_click(self):
        def run():
            pass
        crawl_thread: Thread = Thread(target=run)
        crawl_thread.start()
        pass

    def handle_import_button_click(self):
        res = QFileDialog.getOpenFileNames()[0]
        if len(res) != 0:
            self.file = res[0]
            self.log(log_type="FILE_IMPORT", log_text=f"Path:{self.file}.")
            try:
                self.task = self.read_xlsx()
            except InvalidFileException:
                self.log(log_type="ERROR", log_text=f"File '{self.file}' may not a xlsx file.")
            else:
                self.log(log_type="FILE_IMPORT", log_text="Xlsx file import success.")
        else:
            self.log(log_type="FILE_IMPORT", log_text="Cancel")
        pass

    def handle_log_signal(self, log_type, log_text):
        self.log_box.addItem(f"[{log_type}] {log_text}")
        pass

    def handle_update_progress_bar_signal(self, progress):
        self.progress_bar.setValue(progress)
        pass

    def log(self, log_type, log_text):
        self.log_box.addItem(f"[{log_type}] {log_text}")
        pass

    def read_xlsx(self) -> dict:
        wb: Workbook = openpyxl.open(filename=self.file)
        ws: Worksheet = wb.worksheets[0]
        self.task_list = []
        row: int = 2
        while ws.cell(row, 1).value is not None:
            self.task_list.append(ws.cell(row, 1).value)
            row = row + 1
        return {
            'task_count': row,
            'task_list': self.task_list
        }



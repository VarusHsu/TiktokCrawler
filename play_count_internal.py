import sys

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QProgressBar, QFileDialog

from feishu import Feishu
from logger import Logger
from reporter import Reporter
from requester import Requester
from signals import UpdateUISignals, AdjustConfigSignals
from xlsx_worker import XlsxWorker, init_writer, init_reader
from generate_path import default_path


class ConfigWindows(QObject):
    # ui_widget
    windows: QWidget
    save_button: QPushButton
    cancel_button: QPushButton

    # signals
    update_ui_signals: UpdateUISignals
    adjust_config_signals: AdjustConfigSignals

    def __init__(self, update_ui_signals: UpdateUISignals, adjust_config_signals: AdjustConfigSignals):
        super().__init__()
        self.update_ui_signals = update_ui_signals
        self.adjust_config_signals = adjust_config_signals

    def render(self):
        self.windows = QWidget()
        self.windows.setWindowTitle("Setting")
        self.windows.resize(500, 314)
        self.windows.setFixedSize(500, 314)

        self.save_button = QPushButton(self.windows)
        self.save_button.setText("Save")
        self.save_button.move(20, 280)

        self.cancel_button = QPushButton(self.windows)
        self.cancel_button.setText("Cancel")
        self.cancel_button.move(400, 280)

        self.windows.show()

        pass


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
    progress_bar: QProgressBar
    config_windows: ConfigWindows
    import_file_dialog: QFileDialog
    output_path_file_dialog: QFileDialog

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
        self.update_ui_signals.log_signal.connect(self.handle_log_signal)

        self.feishu = Feishu()
        self.logger = Logger(lark_sender=self.feishu, signals_sender=self.update_ui_signals)
        self.requester = Requester(logger=self.logger)

    def render(self):
        self.app = QApplication(sys.argv)
        self.windows = QWidget()
        self.windows.resize(750, 421)
        self.windows.setWindowTitle("Jojoy tiktok played information")
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
        self.import_button.clicked.connect(self.handle_import_button_clicked)

        self.config_button = QPushButton(self.windows)
        self.config_button.setText("Setting")
        self.config_button.move(660, 385)
        self.config_button.clicked.connect(self.handle_config_button_clicked)

        self.progress_bar = QProgressBar(self.windows)
        self.progress_bar.setFixedWidth(710)
        self.progress_bar.move(20, 3)

        self.windows.show()
        sys.exit(self.app.exec())
        pass

    def handle_crawl_button_clicked(self):
        pass

    def handle_import_button_clicked(self):
        self.import_file_dialog = QFileDialog(self.windows)
        filename = self.import_file_dialog.getOpenFileNames()[0]
        if len(filename) == 0:
            self.logger.log_message("IMPORT", "Cancel.")
            return
        else:
            filename = filename[0]
        self.xlsx_reader = init_reader(filename)
        if self.xlsx_reader is None:
            self.logger.log_message("ERROR", f"File '{filename}' may not a xlsx file.")
        else:
            self.logger.log_message("IMPORT", f"File '{filename}' import success.")
        pass

    def handle_config_button_clicked(self):
        self.config_windows = ConfigWindows(self.update_ui_signals, self.adjust_config_signals)
        self.config_windows.render()
        pass

    def handle_log_signal(self, message):
        self.log_box.addItem(message)
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

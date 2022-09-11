import os.path
import sys
from threading import Thread

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QProgressBar, QFileDialog, QLineEdit, QLabel, QCheckBox

from feishu import Feishu
from logger import Logger
from reporter import Reporter
from requester import Requester
from signals import UpdateUISignals, AdjustConfigSignals
from xlsx_worker import XlsxWorker, init_writer, init_reader
from generate_path import default_path


class ConfigWindows(QObject):
    # module
    logger: Logger

    # ui_widget
    windows: QWidget
    save_button: QPushButton
    cancel_button: QPushButton
    output_path_line_edit: QLineEdit
    output_path_label: QLabel
    notice_email_line_edit: QLineEdit
    notice_email_label: QLabel
    output_path_button: QPushButton
    output_path_filedialog: QFileDialog
    notice_enable_checkbox: QCheckBox
    notice_enable_label: QLabel

    # signals
    update_ui_signals: UpdateUISignals
    adjust_config_signals: AdjustConfigSignals

    output_path: str

    def __init__(self, update_ui_signals: UpdateUISignals, adjust_config_signals: AdjustConfigSignals, logger: Logger, output_path):
        super().__init__()
        self.update_ui_signals = update_ui_signals
        self.adjust_config_signals = adjust_config_signals
        self.logger = logger
        self.output_path = output_path

    def render(self):
        self.windows = QWidget()
        self.windows.setWindowTitle("Setting")
        self.windows.resize(500, 314)
        self.windows.setFixedSize(500, 314)

        self.save_button = QPushButton(self.windows)
        self.save_button.setText("Save")
        self.save_button.move(20, 280)
        self.save_button.setFixedWidth(80)
        self.save_button.clicked.connect(self.handle_save_button_clicked)

        self.cancel_button = QPushButton(self.windows)
        self.cancel_button.setText("Cancel")
        self.cancel_button.move(400, 280)
        self.cancel_button.setFixedWidth(80)
        self.cancel_button.clicked.connect(self.handle_cancel_button_clicked)

        self.output_path_label = QLabel(self.windows)
        self.output_path_label.setText("Output directory:")
        self.output_path_label.move(20, 20)

        self.output_path_line_edit = QLineEdit(self.windows)
        self.output_path_line_edit.setText(self.output_path)
        self.output_path_line_edit.setFixedWidth(260)
        self.output_path_line_edit.move(130, 17)

        self.output_path_button = QPushButton(self.windows)
        self.output_path_button.setText("Select")
        self.output_path_button.setFixedWidth(80)
        self.output_path_button.move(400, 13)
        self.output_path_button.clicked.connect(self.handle_select_button_clicked)

        self.notice_email_label = QLabel(self.windows)
        self.notice_email_label.setText("Notice email:")
        self.notice_email_label.move(20, 50)

        self.notice_email_line_edit = QLineEdit(self.windows)
        self.notice_email_line_edit.setFixedWidth(260)
        self.notice_email_line_edit.move(130, 47)

        self.notice_enable_checkbox = QCheckBox(self.windows)
        self.notice_enable_checkbox.move(400, 50)

        self.notice_enable_label = QLabel(self.windows)
        self.notice_enable_label.setText("Enable")
        self.notice_enable_label.move(420, 51)
        self.windows.show()
        pass

    def handle_save_button_clicked(self):
        self.adjust_config_signals.adjust_output_path_signal.emit(self.output_path_line_edit.text())
        if self.notice_enable_checkbox.isChecked():
            self.adjust_config_signals.adjust_notice_email.emit(self.notice_email_line_edit.text())
        else:
            self.adjust_config_signals.adjust_notice_email.emit("")
        pass
        self.windows.close()

    def handle_cancel_button_clicked(self):
        self.logger.log_message("CONFIG", "Cancel.")
        self.windows.close()
        pass

    def handle_select_button_clicked(self):
        self.output_path_filedialog = QFileDialog(self.windows)
        self.output_path_filedialog.setWindowTitle("Select output directory")
        self.output_path_filedialog.setFileMode(QFileDialog.FileMode.Directory)
        self.output_path_filedialog.show()
        directory = self.output_path_filedialog.getExistingDirectory()
        if directory != "":
            self.output_path = directory
        self.output_path_filedialog.close()
        self.output_path_line_edit.setText(self.output_path)
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
    notice_email = ''

    def __init__(self):
        super().__init__()

        self.update_ui_signals = UpdateUISignals()
        self.adjust_config_signals = AdjustConfigSignals()
        self.update_ui_signals.log_signal.connect(self.handle_log_signal)
        self.adjust_config_signals.adjust_output_path_signal.connect(self.handle_update_output_directory_signal)
        self.adjust_config_signals.adjust_notice_email.connect(self.handle_update_notice_email_signal)

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
        self.crawl_button.setFixedWidth(80)
        self.crawl_button.move(20, 385)

        self.import_button = QPushButton(self.windows)
        self.import_button.setText("Open")
        self.import_button.move(330, 385)
        self.import_button.setFixedWidth(80)
        self.import_button.clicked.connect(self.handle_import_button_clicked)

        self.config_button = QPushButton(self.windows)
        self.config_button.setText("Setting")
        self.config_button.move(650, 385)
        self.config_button.setFixedWidth(80)
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
        self.config_windows = ConfigWindows(self.update_ui_signals, self.adjust_config_signals, self.logger, self.output_path)
        self.config_windows.render()
        pass

    def handle_log_signal(self, message):
        self.log_box.addItem(message)
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())

    def handle_update_output_directory_signal(self, path: str):
        ok = self.check_directory_exist(path=path)
        if ok:
            self.logger.log_message("CONFIG", f"Set '{path}' as output path success.")
            self.output_path = path
        else:
            self.logger.log_message("ERROR", f"'{path}' not found.")

    def handle_update_notice_email_signal(self, email):
        if email == "":
            self.logger.log_message("CONFIG", "There will no notice when complete.")
        else:
            def run(notice_email: str):
                ok = self.feishu.verify_email(email=notice_email)
                if ok:
                    self.logger.log_message("CONFIG", f"Notice email '{notice_email}'.")
                    self.notice_email = notice_email
                else:
                    self.logger.log_message("ERROR", f"Check you email spell '{notice_email}'.")
            thread: Thread = Thread(target=run, args=(email,))
            thread.start()

    @staticmethod
    def check_directory_exist(path: str) ->bool:
        return os.path.exists(path)


import os

from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QLabel, QCheckBox, QFileDialog, QPushButton, QLineEdit, QWidget

from common.logger import Logger
from common.signals import UpdateUISignals, AdjustConfigSignals
from generate.generate_path import default_path


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
    hashtag_label: QLabel
    hashtag_line_edit: QLineEdit
    youtube_label: QLabel
    tiktok_label: QLabel
    youtube_checkbox: QCheckBox
    tiktok_checkbox: QCheckBox

    # signals
    update_ui_signals: UpdateUISignals
    adjust_config_signals: AdjustConfigSignals

    is_from_tiktok: bool
    is_from_youtube: bool
    hashtag_str: str
    output_path: str
    is_hashtag: bool

    cache_file: str = default_path + ".crawl_cache"

    def __init__(self, update_ui_signals: UpdateUISignals, adjust_config_signals: AdjustConfigSignals, logger: Logger, output_path: str, is_hashtag: bool, hashtag_str: str, is_from_tiktok: bool = False, is_from_youtube: bool = False):
        super().__init__()
        self.update_ui_signals = update_ui_signals
        self.adjust_config_signals = adjust_config_signals
        self.logger = logger
        self.output_path = output_path
        self.is_hashtag = is_hashtag
        self.hashtag_str = hashtag_str
        self.is_from_tiktok = is_from_tiktok
        self.is_from_youtube = is_from_youtube

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

        # deprecated
        # self.notice_email_label = QLabel(self.windows)
        # self.notice_email_label.setText("Notice email:")
        # self.notice_email_label.move(20, 50)
        #
        # self.notice_email_line_edit = QLineEdit(self.windows)
        # self.notice_email_line_edit.setFixedWidth(260)
        # self.notice_email_line_edit.move(130, 47)
        #
        # self.notice_enable_checkbox = QCheckBox(self.windows)
        # self.notice_enable_checkbox.move(400, 50)
        #
        # self.notice_enable_label = QLabel(self.windows)
        # self.notice_enable_label.setText("Enable")
        # self.notice_enable_label.move(420, 51)

        if self.is_hashtag:
            self.hashtag_label = QLabel(self.windows)
            self.hashtag_label.setText("Hashtag:")
            self.hashtag_label.move(20, 50)

            self.hashtag_line_edit = QLineEdit(self.windows)
            self.hashtag_line_edit.setText(self.hashtag_str)
            self.hashtag_line_edit.setFixedWidth(260)
            self.hashtag_line_edit.move(130, 47)

            self.tiktok_label = QLabel(self.windows)
            self.tiktok_label.setText("Tiktok: ")
            self.tiktok_label.move(20, 80)

            self.youtube_label = QLabel(self.windows)
            self.youtube_label.setText("Youtube: ")
            self.youtube_label.move(20, 110)

            self.tiktok_checkbox = QCheckBox(self.windows)
            self.tiktok_checkbox.move(130, 80)
            self.tiktok_checkbox.clicked.connect(self.handle_tiktok_checkbox_clicked)
            self.tiktok_checkbox.setChecked(self.is_from_tiktok)

            self.youtube_checkbox = QCheckBox(self.windows)
            self.youtube_checkbox.move(130, 110)
            self.youtube_checkbox.clicked.connect(self.handle_youtube_checkbox_clicked)
            self.youtube_checkbox.setChecked(self.is_from_youtube)

        self.windows.show()
        pass

    def handle_save_button_clicked(self):
        self.adjust_config_signals.adjust_output_path_signal.emit(self.output_path_line_edit.text())
        # deprecated
        # if self.notice_enable_checkbox.isChecked():
        #     self.adjust_config_signals.adjust_notice_email.emit(self.notice_email_line_edit.text())
        # else:
        #     self.adjust_config_signals.adjust_notice_email.emit("")
        if self.is_hashtag:
            self.adjust_config_signals.adjust_hashtag.emit(self.hashtag_line_edit.text())
            self.adjust_config_signals.adjust_hashtag_website_signal.emit(self.is_from_tiktok, self.is_from_youtube)
            self.set_default_website(self.is_from_tiktok, self.is_from_youtube)
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

    def get_default_website(self):
        try:
            with open(self.cache_file, "r") as f:
                cache = f.read(2)
                self.is_from_tiktok = cache[0] == '1'
                self.is_from_youtube = cache[1] == '1'
        except FileNotFoundError:
            self.generate_default_website()
            self.get_default_website()
        pass

    def generate_default_website(self):
        with open(self.cache_file, "w") as f:
            f.write("10")
        pass

    def set_default_website(self, is_from_tiktok: bool, is_from_youtube: bool):
        res = ""
        if is_from_tiktok:
            res += "1"
        else:
            res += "0"
        if is_from_youtube:
            res += "1"
        else:
            res += "0"
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        with open(self.cache_file, "w") as f:
            f.write(res)

    def handle_youtube_checkbox_clicked(self):
        self.is_from_youtube = self.youtube_checkbox.isChecked()
        if not self.is_from_youtube and not self.is_from_tiktok:
            self.save_button.setEnabled(False)
        else:
            self.save_button.setEnabled(True)
        pass

    def handle_tiktok_checkbox_clicked(self):
        self.is_from_tiktok = self.tiktok_checkbox.isChecked()
        if not self.is_from_youtube and not self.is_from_tiktok:
            self.save_button.setEnabled(False)
        else:
            self.save_button.setEnabled(True)
        pass



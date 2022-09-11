from PyQt6.QtCore import QObject, pyqtSignal


class UpdateUISignals(QObject):
    log_signal = pyqtSignal(str)
    progress_bar_update_signal = pyqtSignal()


class AdjustConfigSignals(QObject):
    adjust_output_path_signal = pyqtSignal(str)
    adjust_begin_line_signal = pyqtSignal(int)    # deprecated
    adjust_notice_email = pyqtSignal(str)

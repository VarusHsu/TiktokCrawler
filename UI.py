from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QFileDialog
import sys

# 窗口size
window_width: int = 500
window_height: int = 314

# 按钮size
button_width: int = 80
button_height: int = 20

# 边沿长度
edge_distance: int = 20

window: QWidget
crawl_button: QPushButton
import_button: QPushButton
text_box: QTextEdit
test_button: QPushButton
file: str


# 渲染UI
def render_ui():
    # 获取窗口
    app = QApplication(sys.argv)
    global window
    window = QWidget()

    # 设置标题，尺寸和禁用拉伸
    window.resize(window_width, window_height)
    window.setWindowTitle("短视频播放量爬虫（0.0）")
    window.setFixedSize(window.width(), window.height())

    # 文本框
    global text_box
    text_box = QTextEdit(window)
    text_box.move(edge_distance, edge_distance)
    text_box.resize(window_width - 2 * edge_distance, window_height - button_height - 3 * edge_distance)
    text_box.setReadOnly(True)

    # 爬取按钮
    global crawl_button
    crawl_button = QPushButton(window)
    crawl_button.setText("开始爬取")
    crawl_button.move(int(window_width / 3 * 2 - button_width / 2), int(window_height - edge_distance - button_height))
    crawl_button.clicked.connect(handle_crawl_button_click)

    # 导入按钮
    global import_button
    import_button = QPushButton(window)
    import_button.setText("导入表格")
    import_button.move(int(window_width / 3 * 1 - button_width / 2), int(window_height - edge_distance - button_height))
    import_button.clicked.connect(handle_import_button_click)

    window.show()
    sys.exit(app.exec())


def handle_crawl_button_click():
    run_log("run")
    pass


def handle_import_button_click():
    global file
    res = QFileDialog.getOpenFileNames()[0]
    if len(res) != 0:
        file = res[0]
        run_log(f"[FILE_IMPORT] Path:{file}")
    else:
        run_log(f"[FILE_IMPORT] Cancel")


def handle_test_button_click():
    err_log("err")


def run_log(text: str):
    text_box.setTextColor(QtGui.QColor('#000000'))
    text_box.append(text)


def err_log(text: str):
    text_box.setTextColor(QtGui.QColor('#FF0000'))
    text_box.append(text)

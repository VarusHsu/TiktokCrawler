import time

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit
import sys

# 窗口size
window_width: int = 500
window_height: int = 314

# 按钮size
button_width: int = 80
button_height: int = 20


edge_distance: int = 20


# 渲染UI
def render_ui():
    # 获取窗口
    app = QApplication(sys.argv)
    window = QWidget()

    # 设置标题，尺寸和禁用拉伸
    window.resize(window_width, window_height)
    window.setWindowTitle("短视频播放量爬虫（0.0）")
    window.setFixedSize(window.width(), window.height())

    # 文本框
    text_box = QLineEdit(window)
    text_box.move(edge_distance, edge_distance)
    text_box.resize(window_width - 2 * edge_distance, window_height - button_height - 3 * edge_distance)

    # 爬取按钮
    crawl_button = QPushButton(window)
    crawl_button.setText("开始爬取")
    crawl_button.move(int((window_width - button_width) / 2), int(window_height - edge_distance - button_height))

    window.show()
    sys.exit(app.exec())


def handle_crawl_button_click(text_box):
    text_box.setText("123")

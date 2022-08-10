import openpyxl
import requests
from PyQt6 import QtCore
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QListView
import sys

# 窗口size
from PyQt6.QtCore import QThread, QStringListModel
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet
from requests.exceptions import MissingSchema, SSLError

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
text_box: QListView
test_button: QPushButton
file: str
task: dict = {}
string_list_model = QStringListModel()
logList = ['[Welcome] QAQ']
string_list_model.setStringList(logList)


font: QFont = QFont("Consolas")

colors = {
    "RED": "#ff0000",
    "BLACK": "#000000"
}


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
    global font
    text_box = QListView(window)
    text_box.move(edge_distance, edge_distance)
    text_box.resize(window_width - 2 * edge_distance, window_height - button_height - 3 * edge_distance)
    text_box.setModel(string_list_model)
    text_box.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
    crawl_thread = CrawlThread(window)
    crawl_thread.start()


def handle_import_button_click():
    global file
    res = QFileDialog.getOpenFileNames()[0]
    if len(res) != 0:
        file = res[0]
        log(f"[FILE_IMPORT] Path:{file}")
        try:
            global task
            task = read_xlsx()
        except InvalidFileException:
            log(f"[ERROR] File '{file}' may not a xlsx file")
        else:
            log(f"[FILE_IMPORT] Xlsx file import success")
    else:
        log(f"[FILE_IMPORT] Cancel")


def log(text: str, color: str = colors["BLACK"]):
    # todo  这里继续加字体颜色
    logList.append(text)
    string_list_model.setStringList(logList)
    text_box.setModel(string_list_model)
    text_box.verticalScrollBar().setValue(text_box.verticalScrollBar().maximum())


def request_get(url: str, allow_redirects: bool):
    try:
        response = requests.get(url, allow_redirects=allow_redirects)
    except MissingSchema:
        log(f"[ERROR] Invalid URL '{url}', perhaps you meant 'https://{url}'")
        return None
    except SSLError:
        log(f"[ERROR] Max retries exceeded with URL '{url}'")
        pass
    else:
        if response.status_code == 200 or response.status_code == 301:
            log(f"[GET] {response.status_code}: {url}")
            return response.content
        else:
            log(f"[GET] {response.status_code}: {url}")
            return None


def get_url_type(url: str):
    if url.startswith("https://vm.tiktok.com"):
        return "solution_1"
    else:
        log(f"[ERROR] Invalid URL '{url}'")
        return ""


def solution_1(url: str):
    response = request_get(url=url, allow_redirects=False)
    if response is None:
        return
    soup = BeautifulSoup(response, "lxml")
    redirect_url = soup.find(name="a")["href"]
    response = request_get(redirect_url, allow_redirects=True)
    print(response)


def read_xlsx() -> dict:
    wb: Workbook = openpyxl.open(filename=file)
    ws: Worksheet = wb.worksheets[0]
    task_list = []
    row: int = 2
    while ws.cell(row, 1).value is not None:
        task_list.append(ws.cell(row, 1).value)
        row = row + 1
    return {
        'task_count': row,
        'task_list': task_list
    }


class CrawlThread (QThread):
    def run(self):
        global task
        if task == {}:
            log("[ERROR] None file imported")
        else:
            log("[BEGIN] Crawl start")
            for url in task.get("task_list"):
                url_type = get_url_type(url=url)
                if url_type == "solution_1":
                    solution_1(url)


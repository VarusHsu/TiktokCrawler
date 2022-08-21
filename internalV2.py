import json
import sys
from threading import Thread


import requests
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication, QPushButton, QProgressBar, QListWidget, QWidget, QFileDialog
from PyQt6 import QtCore
from bs4 import BeautifulSoup
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import openpyxl
from requests.exceptions import MissingSchema, SSLError


class UpdateUISignals(QObject):
    log_signal = pyqtSignal(str, str)
    progress_bar_update_signal = pyqtSignal()


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
    progress: int = 0
    output_path: str = "/Users/rockey211224/Desktop/output.xlsx"

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
            if self.task == {}:
                self.update_ui_signals.log_signal.emit("ERROR", "None file imported.")
            else:
                self.update_ui_signals.log_signal.emit("BEGIN", "Crawl start")
                wb = openpyxl.Workbook()
                self.write_res_header(wb=wb)
                for url in self.task.get("task_list"):
                    url_type = self.get_url_type(url=url)
                    if url_type == "tiktok_without_video_id":
                        res = self.tiktok_without_video_id_proc(url)
                    elif url_type == "tiktok_with_video_id":
                        res = self.tiktok_with_video_id_proc(url)
                    else:
                        res = {
                            "found": -2,
                            "video_id": "",
                            "share": 0,
                            "play": 0,
                            "digg": 0,
                            "comment": 0,
                        }
                    self.write_res_line(wb=wb,
                                        row=self.progress + 2,
                                        url=url,
                                        video_id=res["video_id"],
                                        comment=res["comment"],
                                        like=res["digg"],
                                        play=res["play"],
                                        share=res["share"],
                                        status=res["found"]
                                        )
                    self.update_ui_signals.progress_bar_update_signal.emit()
                    self.progress = self.progress + 1
                self.update_ui_signals.log_signal.emit("COMPLETE", "Crawl complete.")

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
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())
        pass

    def handle_update_progress_bar_signal(self):
        self.progress_bar.setValue(int(self.progress / (len(self.task["task_list"]) - 1) * 100))
        pass

    def log(self, log_type, log_text):
        self.log_box.addItem(f"[{log_type}] {log_text}")
        self.log_box.verticalScrollBar().setValue(self.log_box.verticalScrollBar().maximum())
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

    def write_res_line(self, wb: Workbook, row: int, url: str, video_id: str, status: int, like: int, comment: int, share: int, play: int):
        status_dict = {
            -1: "联系徐硕改代码",
            1: "Success",
            0: "Video lose efficacy",
            -2: "Bad URL or this website has no solution"
        }
        wb.worksheets[0].cell(row=row, column=1, value=url)
        wb.worksheets[0].cell(row=row, column=2, value=video_id)
        wb.worksheets[0].cell(row=row, column=3, value=status_dict[status])
        wb.worksheets[0].cell(row=row, column=4, value=like)
        wb.worksheets[0].cell(row=row, column=5, value=comment)
        wb.worksheets[0].cell(row=row, column=6, value=share)
        wb.worksheets[0].cell(row=row, column=7, value=play)
        wb.save(filename=self.output_path)
        self.log(log_type="SAVE", log_text=f"Save id = {video_id} success.")

    def write_res_header(self, wb: Workbook):
        wb.worksheets[0].cell(row=1, column=1, value="URL")
        wb.worksheets[0].cell(row=1, column=2, value="VideoID")
        wb.worksheets[0].cell(row=1, column=3, value="Status")
        wb.worksheets[0].cell(row=1, column=4, value="LikesCount")
        wb.worksheets[0].cell(row=1, column=5, value="CommentsCount")
        wb.worksheets[0].cell(row=1, column=6, value="SharesCount")
        wb.worksheets[0].cell(row=1, column=7, value="PlaysCount")
        wb.save(filename=self.output_path)
        self.log(log_type="SAVE", log_text="Save header success")

    def get_url_type(self, url: str):
        if url.startswith("https://vm.tiktok.com") or url.startswith("https://vt.tiktok.com"):
            return "tiktok_without_video_id"
        elif url.startswith("https://www.tiktok.com"):
            return "toktok_with_video_id"
        self.log(log_type="ERROR", log_text=f"Invalid URL '{url}'.")
        return ""

    def tiktok_without_video_id_proc(self, url: str):
        response = self.request_get(url=url, allow_redirects=False)
        if response is None:
            return
        soup = BeautifulSoup(response, "lxml")
        redirect_url = soup.find(name="a")["href"]
        video_id = self.get_tiktok_video_id(redirect_url)
        url = "https://www.tiktok.com/api/recommend/item_list/?aid=1988&app_language=es&app_name=tiktok_web&battery_info=0.44&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&device_id=7106463322559923714&device_platform=web_pc&focus_state=true&from_page=video&history_len=1&insertedItemID=" + video_id + "&is_fullscreen=true&is_page_visible=true&os=mac&priority_region=&referer=&region=DE&screen_height=1920&screen_width=1080&tz_name=Asia%2FShanghai&webcast_language=es&msToken=" + self.ms_token
        response = self.request_get(url=url, allow_redirects=False)
        if response is None:
            return
        rsp_json = json.loads(response)
        res = self.get_tiktok_data_from_api(except_id=video_id, rsp_json=rsp_json)
        if res["found"] == 1:
            self.update_ui_signals.log_signal.emit("SUCCESS", f"Get video:{video_id}; share: {res['share']}; play: {res['play']}; like: {res['digg']}; comment: {res['comment']}")
        elif res["found"] == 0:
            self.update_ui_signals.log_signal.emit("FAILED", "This video may lose efficacy")
        else:
            self.update_ui_signals.log_signal.emit("FAILED", "Api response may issue")
        return res

    def request_get(self, url: str, allow_redirects: bool):
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        try:
            response = requests.get(url, allow_redirects=allow_redirects, headers=headers)
        except MissingSchema:
            self.update_ui_signals.log_signal.emit("ERROR", f"Invalid URL '{url}', perhaps you meant 'https://{url}'.")
            return None
        except SSLError:
            self.update_ui_signals.log_signal.emit("ERROR", f"Max retries exceeded with URL '{url}'.")
            pass
        except requests.exceptions.ConnectionError:
            self.update_ui_signals.log_signal.emit("ERROR", "Internet error, maybe this error cause by VPN.")
        else:
            if response.status_code == 200 or response.status_code == 301:
                self.update_ui_signals.log_signal.emit("GET", f"{response.status_code}: {url}.")
                return response.content
            elif response.status_code == 404:
                return 404
            else:
                self.update_ui_signals.log_signal.emit("GET", f"{response.status_code}: {url}.")
                return None

    def get_tiktok_video_id(self, url: str) -> str:
        res_begin_index: int = url.rfind("/")
        res_end_index: int = url.find("?")
        res = url[res_begin_index + 1:res_end_index]
        for letter in res:
            if letter.isalpha():
                return ""
        return res

    def get_tiktok_data_from_api(self, except_id: str, rsp_json: dict) -> dict:
        try:
            item_list = rsp_json["itemList"]
            for item in item_list:
                if item["id"] == except_id:
                    share = item["stats"]["shareCount"]
                    play = item["stats"]["playCount"]
                    digg = item["stats"]["diggCount"]
                    comment = item["stats"]["commentCount"]
                    return {
                        "found": 1,
                        "video_id": except_id,
                        "share": share,
                        "play": play,
                        "digg": digg,
                        "comment": comment
                    }
            return {
                "found": 0,
                "video_id": except_id,
                "share": 0,
                "play": 0,
                "digg": 0,
                "comment": 0,
            }
        except KeyError:
            return {
                "found": -1,
                "video_id": except_id,
                "share": 0,
                "play": 0,
                "digg": 0,
                "comment": 0,
            }

    def tiktok_with_video_id_proc(self, url:str):
        video_id = self.get_tiktok_video_id(url)
        url_ = "https://www.tiktok.com/api/recommend/item_list/?aid=1988&app_language=es&app_name=tiktok_web&battery_info=0.44&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&device_id=7106463322559923714&device_platform=web_pc&focus_state=true&from_page=video&history_len=1&insertedItemID=" + video_id + "&is_fullscreen=true&is_page_visible=true&os=mac&priority_region=&referer=&region=DE&screen_height=1920&screen_width=1080&tz_name=Asia%2FShanghai&webcast_language=es&msToken=" + ms_token
        response = self.request_get(url=url_, allow_redirects=False)
        if response is None:
            return
        rsp_json = json.loads(response)
        res = self.get_tiktok_data_from_api(except_id=video_id, rsp_json=rsp_json)
        if res["found"] == 1:
            self.update_ui_signals.log_signal.emit("SUCCESS", f"Get video:{video_id}; share: {res['share']}; play: {res['play']}; like: {res['digg']}; comment: {res['comment']}.")
        elif res["found"] == 0:
            self.update_ui_signals.log_signal.emit("FAILED", "This video may lose efficacy")
        else:
            self.update_ui_signals.log_signal.emit("FAILED", "Api response may issue")
        return res


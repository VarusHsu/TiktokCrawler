import json
import os.path
import sys
import time
from threading import Thread

from PyQt6 import QtCore
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QApplication, QWidget, QListWidget, QPushButton, QProgressBar, QFileDialog
from bs4 import BeautifulSoup

from config_windows import ConfigWindows
from feishu import Feishu
from logger import Logger
from reporter import Reporter
from requester import Requester
from signals import UpdateUISignals, AdjustConfigSignals
from xlsx_worker import XlsxWorker, init_writer, init_reader
from generate_path import default_path

from enums import XlsxReadStatus, UrlType, VideoResponseStatus,HttpResponseStatus


class PlayCountCrawler(QObject):
    # module
    feishu: Feishu
    reporter: Reporter
    requester: Requester
    logger: Logger
    xlsx_reader: XlsxWorker = None
    xlsx_writer: XlsxWorker = None

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
    ms_token = 'g8vXKy2fjhjd7xrrPcCU7Wfop7isL5KAuyjofBp061Mtaxm_fA5vZ_lAlj46mvE_NnR7x-m-022QnOLdb6Em6HbYv1qm-ek2LXKHh6aTtnLpk_Ke8h7MUTkvWAUZX0cQ1JhrowY='

    def __init__(self):
        super().__init__()

        self.update_ui_signals = UpdateUISignals()
        self.adjust_config_signals = AdjustConfigSignals()
        self.update_ui_signals.log_signal.connect(self.handle_log_signal)
        self.adjust_config_signals.adjust_output_path_signal.connect(self.handle_update_output_directory_signal)
        self.adjust_config_signals.adjust_notice_email.connect(self.handle_update_notice_email_signal)
        self.update_ui_signals.progress_bar_update_signal.connect(self.handle_update_progress_bar_signal)

        self.feishu = Feishu()
        self.logger = Logger(lark_sender=self.feishu, signals_sender=self.update_ui_signals)
        self.requester = Requester(logger=self.logger)
        self.reporter = Reporter()

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
        self.crawl_button.clicked.connect(self.handle_crawl_button_clicked)

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
        def run():
            fields = ("Url", "Status", "VideoId", "Comment", "Share", "Played", "Digg")
            filename = self.get_abs_output_filename()
            self.xlsx_writer = init_writer(path=filename, fields=fields)
            if self.xlsx_reader is None:
                self.logger.log_message("ERROR", "Open a xlsx file first.")
                return
            self.progress_bar.setValue(0)
            self.logger.log_message("BEGIN", "Crawl start.")
            self.reporter.set_timer()
            while True:
                read_res = self.xlsx_reader.read_url()
                if read_res.status == XlsxReadStatus.NoMoreData:
                    break
                elif read_res.status == XlsxReadStatus.PermissionDenied:
                    self.logger.log_message("ERROR", "Permission denied.")
                elif read_res.status == XlsxReadStatus.Invalid:
                    self.logger.log_message("ERROR", "Invalid.")
                else:
                    url = read_res.url
                    self.logger.log_message("CRAWL", f"Process '{url}'.")
                    url_type = self.get_url_type(url)
                    if url_type == UrlType.Invalid:
                        self.logger.log_message("ERROR", f"Invalid url '{url}'.")
                        continue
                    elif url_type == UrlType.VtTiktokCom:
                        res = self.vt_tiktok_com(url)
                    elif url_type == UrlType.VmTiktokCom:
                        res = self.vm_tiktok_com(url)
                    elif url_type == UrlType.WwwTiktokCom:
                        res = self.www_tiktok_com(url)
                    else:
                        res = self.www_tiktok_com_t(url)
                    res["Url"] = url
                    self.xlsx_writer.writer_line(res)
                    self.update_ui_signals.progress_bar_update_signal.emit(int((self.xlsx_reader.cur_line-1)/self.xlsx_reader.total_rows * 100))
            time.sleep(3)
            during = self.reporter.get_during()
            self.logger.log_message("SUMMERY", f"Cost {during/1000} s")
            self.logger.log_message("COMPLETE", "Complete.", self.notice_email)

        crawl_thread: Thread = Thread(target=run)
        crawl_thread.start()
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
        self.config_windows = ConfigWindows(self.update_ui_signals, self.adjust_config_signals, self.logger, self.output_path, False, "")
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

    def handle_update_progress_bar_signal(self, progress):
        self.progress_bar.setValue(progress)

    @staticmethod
    def check_directory_exist(path: str) ->bool:
        return os.path.exists(path)

    def get_abs_output_filename(self) ->str:
        if self.output_path.endswith("/"):
            return self.output_path + time.strftime("%Y-%m-%d_%H:%M:%S.xlsx", time.localtime())
        else:
            return self.output_path + "/" + time.strftime("%Y-%m-%d_%H:%M:%S.xlsx", time.localtime())

    @staticmethod
    def get_url_type(url: str) -> UrlType:
        if url.startswith("https://www.tiktok.com/t"):
            return UrlType.WwwTiktokComT
        elif url.startswith("https://vm.tiktok.com"):
            return UrlType.VmTiktokCom
        elif url.startswith("https://vt.tiktok.com"):
            return UrlType.VtTiktokCom
        elif url.startswith("https://www.tiktok.com"):
            return UrlType.WwwTiktokCom
        else:
            return UrlType.Invalid

    def vm_tiktok_com(self, url: str):
        network_error_rsp: dict = {
                "Url": url,
                "Status": VideoResponseStatus.NetWorkError,
                "VideoId": None,
                "Share": None,
                "Played": None,
                "Digg": None,
                "Comment": None,
            }
        response = self.requester.get(url=url, allow_redirects=False)
        if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
            return network_error_rsp
        soup = BeautifulSoup(response.content, "lxml")
        url = soup.find(name="a")["href"]
        video_id = self.get_tiktok_video_id(url)
        network_error_rsp["VideoId"] = video_id
        url = "https://www.tiktok.com/api/recommend/item_list/?aid=1988&app_language=es&app_name=tiktok_web&battery_info=0.44&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&device_id=7106463322559923714&device_platform=web_pc&focus_state=true&from_page=video&history_len=1&insertedItemID=" + video_id + "&is_fullscreen=true&is_page_visible=true&os=mac&priority_region=&referer=&region=DE&screen_height=1920&screen_width=1080&tz_name=Asia%2FShanghai&webcast_language=es&msToken=" + self.ms_token
        response = self.requester.get(url=url, allow_redirects=False)
        if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
            return network_error_rsp
        rsp_json = json.loads(response.content)
        res = self.get_tiktok_data_from_api(video_id, rsp_json)
        return res

    def vt_tiktok_com(self, url: str):
        return self.vm_tiktok_com(url)

    def www_tiktok_com(self, url: str):
        network_error_rsp: dict = {
                "Url": url,
                "Status": VideoResponseStatus.NetWorkError,
                "VideoId": None,
                "Share": None,
                "Played": None,
                "Digg": None,
                "Comment": None,
            }
        video_id = self.get_tiktok_video_id(url)
        url = "https://www.tiktok.com/api/recommend/item_list/?aid=1988&app_language=es&app_name=tiktok_web&battery_info=0.44&browser_language=zh-CN&browser_name=Mozilla&browser_online=true&browser_platform=MacIntel&browser_version=5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F104.0.0.0%20Safari%2F537.36&channel=tiktok_web&cookie_enabled=true&count=30&device_id=7106463322559923714&device_platform=web_pc&focus_state=true&from_page=video&history_len=1&insertedItemID=" + video_id + "&is_fullscreen=true&is_page_visible=true&os=mac&priority_region=&referer=&region=DE&screen_height=1920&screen_width=1080&tz_name=Asia%2FShanghai&webcast_language=es&msToken=" + self.ms_token
        response = self.requester.get(url=url,allow_redirects=False)
        if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
            return network_error_rsp
        rsp_json = json.loads(response.content)
        res = self.get_tiktok_data_from_api(except_id=video_id, rsp_json=rsp_json)
        return res

    def www_tiktok_com_t(self, url: str):
        return self.vm_tiktok_com(url)

    @staticmethod
    def get_tiktok_video_id(url: str) -> str:
        if url.startswith("https://m.tiktok.com/v/"):
            return url[23: 42]
        elif url.startswith("https://t.tiktok.com/i18n/share/video/"):
            len("https://t.tiktok.com/i18n/share/video/")
            return url[38: 57]
        res_begin_index: int = url.rfind("/")
        if url.find("?") != -1:
            res_end_index: int = url.find("?")
        else:
            res_end_index = len(url)
        res = url[res_begin_index + 1:res_end_index]
        for letter in res:
            if letter.isalpha():
                return ""
        return res

    @staticmethod
    def get_tiktok_data_from_api(except_id: str, rsp_json: dict) -> dict:
        try:
            item_list = rsp_json["itemList"]
            for item in item_list:
                if item["id"] == except_id:
                    share = item["stats"]["shareCount"]
                    play = item["stats"]["playCount"]
                    digg = item["stats"]["diggCount"]
                    comment = item["stats"]["commentCount"]
                    return {
                        "Status": VideoResponseStatus.Success,
                        "VideoId": except_id,
                        "Share": share,
                        "Played": play,
                        "Digg": digg,
                        "Comment": comment
                    }
            return {
                "Status": VideoResponseStatus.LoseEfficacy,
                "VideoId": except_id,
                "Share": None,
                "Played": None,
                "Digg": None,
                "Comment": None,
            }
        except KeyError:
            return {
                "Status": VideoResponseStatus.ApiDataFormatError,
                "VideoId": except_id,
                "Share": None,
                "Played": None,
                "Digg": None,
                "Comment": None,
            }

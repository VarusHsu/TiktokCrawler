import datetime
import sys

sys.path.append(".")

from common.logger import Logger
from common.feishu import Feishu
from common.xlsx_worker import init_reader, compare

path = '/home/ubuntu/TiktokCrawler/server/history/compare_cache/'

feishu = Feishu("https://open.feishu.cn/open-apis/bot/v2/hook/61f8efec-d13b-47a6-8366-697b5db500ec")
logger = Logger(None, feishu)


def main():
    yesterday_xlsx = init_reader(path + get_filename())
    if yesterday_xlsx is None:
        logger.log_message("ERROR", "Read yesterday data error.")
        return
    today_xlsx = init_reader(path + get_yesterday_filename())
    if today_xlsx is None:
        logger.log_message("ERROR", "Read today data error.")
        return
    file_name = str(datetime.date.today() + datetime.timedelta(-1)) + "~" + str(datetime.date.today()) + ".xlsx"
    compare(yesterday_xlsx, today_xlsx, file_name)
    logger.log_message("Success", "Generate increase data success.")
    pass


def get_filename() -> str:
    now = datetime.datetime.now()
    beijing_time = now + datetime.timedelta(hours=8)
    beijing_time_str = datetime.datetime.strftime(beijing_time, "%Y-%m-%d.xlsx")
    return beijing_time_str


def get_yesterday_filename() -> str:
    now = datetime.datetime.now()
    beijing_time = now + datetime.timedelta(hours=-16)
    beijing_time_str = datetime.datetime.strftime(beijing_time, "%Y-%m-%d.xlsx")
    return beijing_time_str


if __name__ == '__main__':
    main()

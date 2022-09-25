import json
import time

from bs4 import BeautifulSoup

from generate import generate_path
from common.xlsx_worker import init_writer, init_reader
from source import source_path
from common.logger import Logger
from common.feishu import Feishu
from common.reporter import Reporter
from common.enums import XlsxReadStatus, UrlType, VideoResponseStatus, HttpResponseStatus
from common.requester import Requester

ms_token = 'g8vXKy2fjhjd7xrrPcCU7Wfop7isL5KAuyjofBp061Mtaxm_fA5vZ_lAlj46mvE_NnR7x-m-022QnOLdb6Em6HbYv1qm-ek2LXKHh6aTtnLpk_Ke8h7MUTkvWAUZX0cQ1JhrowY='


def run():
    fields = ("Url", "Status", "VideoId", "Comment", "Share", "Played", "Digg")
    filename = get_abs_output_filename()
    feishu = Feishu(robot_url="https://open.feishu.cn/open-apis/bot/v2/hook/61f8efec-d13b-47a6-8366-697b5db500ec")
    logger = Logger(lark_sender=feishu, signals_sender=None)
    reporter = Reporter()
    requester = Requester(logger)
    xlsx_writer = init_writer(path=filename, fields=fields)
    xlsx_reader = init_reader(source_path)
    logger.log_message("begin", "Server crawl start.")
    reporter.set_timer()
    while True:
        read_res = xlsx_reader.read_url()
        if read_res.status == XlsxReadStatus.NoMoreData:
            break
        elif read_res.status == XlsxReadStatus.PermissionDenied:
            logger.log_message("ERROR", "Permission denied.")
        elif read_res.status == XlsxReadStatus.Invalid:
            logger.log_message("ERROR", "Invalid.")
        else:
            url = read_res.url
            logger.log_message("CRAWL", f"Process '{url}'.")
            url_type = get_url_type(url)
            if url_type == UrlType.Invalid:
                logger.log_message("ERROR", f"Invalid url '{url}'.")
                continue
            elif url_type == UrlType.VtTiktokCom:
                res = vt_tiktok_com(url, requester)
            elif url_type == UrlType.VmTiktokCom:
                res = vm_tiktok_com(url, requester)
            elif url_type == UrlType.WwwTiktokCom:
                res = www_tiktok_com(url, requester)
            elif url_type == UrlType.KuaiVideoCom:
                res = kuai_video_com(url, requester)
            else:
                res = www_tiktok_com_t(url, requester)
            res["Url"] = url
            xlsx_writer.writer_line(res)
    time.sleep(3)
    during = reporter.get_during()
    logger.log_message("SUMMERY", f"Cost {during / 1000} s")
    logger.log_message("COMPLETE", "Complete.")


def get_abs_output_filename() -> str:
    return generate_path.default_path + time.strftime("%Y-%m-%d_%H:%M:%S.xlsx", time.localtime())


def get_url_type(url: str):
    if url.startswith("https://www.tiktok.com/t"):
        return UrlType.WwwTiktokComT
    elif url.startswith("https://vm.tiktok.com"):
        return UrlType.VmTiktokCom
    elif url.startswith("https://vt.tiktok.com"):
        return UrlType.VtTiktokCom
    elif url.startswith("https://www.tiktok.com"):
        return UrlType.WwwTiktokCom
    elif url.startswith("https://kwai-video.com"):
        return UrlType.KuaiVideoCom
    else:
        return UrlType.Invalid
    pass


def vm_tiktok_com(url: str, requester: Requester):
    network_error_rsp: dict = {
        "Url": url,
        "Status": VideoResponseStatus.NetWorkError,
        "VideoId": None,
        "Share": None,
        "Played": None,
        "Digg": None,
        "Comment": None,
    }
    response = requester.get(url=url, allow_redirects=False)
    if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
        return network_error_rsp
    soup = BeautifulSoup(response.content, "lxml")
    url = soup.find(name="a")["href"]
    video_id = get_tiktok_video_id(url)
    network_error_rsp["VideoId"] = video_id
    url = 'https://www.tiktok.com/api/recommend/item_list/?aid=1988&count=30&insertedItemID=' + video_id + "&msToken=" + ms_token
    response = requester.get(url=url, allow_redirects=False)
    if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
        return network_error_rsp
    rsp_json = json.loads(response.content)
    res = get_tiktok_data_from_api(video_id, rsp_json)
    return res


def vt_tiktok_com(url: str, requester: Requester):
    return vm_tiktok_com(url, requester)


def www_tiktok_com(url: str, requester: Requester):
    network_error_rsp: dict = {
        "Url": url,
        "Status": VideoResponseStatus.NetWorkError,
        "VideoId": None,
        "Share": None,
        "Played": None,
        "Digg": None,
        "Comment": None,
    }
    video_id = get_tiktok_video_id(url)
    url = 'https://www.tiktok.com/api/recommend/item_list/?aid=1988&count=30&insertedItemID=' + video_id + "&msToken=" + ms_token
    response = requester.get(url=url, allow_redirects=False)
    if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
        return network_error_rsp
    rsp_json = json.loads(response.content)
    res = get_tiktok_data_from_api(except_id=video_id, rsp_json=rsp_json)
    return res


def www_tiktok_com_t(url: str, requester: Requester):
    return vm_tiktok_com(url, requester)


def kuai_video_com(url, requester: Requester):
    error_rsp: dict = {
        "Url": url,
        "VideoId": None,
        "Share": None,
        "Played": None,
        "Digg": None,
        "Comment": None,
    }
    response = requester.get(url=url, allow_redirects=True)
    if response.http_status not in [HttpResponseStatus.Success, HttpResponseStatus.Redirects]:
        error_rsp["Status"] = VideoResponseStatus.NetWorkError
        return error_rsp
    soup = BeautifulSoup(response.content, 'lxml')
    meta_info = found_meta(soup)
    if meta_info is None:
        error_rsp["Status"] = VideoResponseStatus.MetaNotFound
        return error_rsp
    url = "https://m.kwai.com/rest/o/w/photo/getUserHotPhoto?kpn=KWAI"
    response = requester.post(url=url, json=meta_info)
    if response.http_status != HttpResponseStatus.Success:
        error_rsp["Status"] = VideoResponseStatus.NetWorkError
        return error_rsp
    rsp_json = json.loads(response.content)
    if rsp_json.get("result") == 1016001002:
        return {
            "Status": VideoResponseStatus.LoseEfficacy,
            "Url": url,
            "VideoId": None,
            "Share": None,
            "Played": None,
            "Digg": None,
            "Comment": None,
        }
    for data in rsp_json["datas"]:
        if data["photoId"] == meta_info["photoId"] and data["userId"] == meta_info["authorId"]:
            return {
                "Status": VideoResponseStatus.Success,
                "VideoId": data["photoId"],
                "Share": None,
                "Played": data["viewCount"],
                "Digg": data["likeCount"],
                "Comment": data["commentCount"],
            }
    return {
        "Status": VideoResponseStatus.LoseEfficacy,
        "Url": url,
        "VideoId": None,
        "Share": None,
        "Played": None,
        "Digg": None,
        "Comment": None,
    }


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


def found_meta(soup):
    soup.findAll(name="meta")
    metas = soup.findAll(name="meta")
    for meta in metas:
        if meta.get("property") == "og:url":
            url = meta.get("content")
            url = url[25:]
            step_index = url.find("/")
            end_index = url.find("?")
            user_id = url[0: step_index]
            photo_id = url[step_index + 1: end_index]
            return {
                "authorId": user_id,
                "photoId": photo_id,
            }
    return None


if __name__ == '__main__':
    run()
    pass

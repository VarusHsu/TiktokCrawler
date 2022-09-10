import time

import requests
from requests.exceptions import MissingSchema, SSLError
from enums import HttpResponseStatus

from logger import Logger


class HttpResponse:
    http_status: HttpResponseStatus
    content: str

    def __init__(self, http_status, content):
        self.content = content
        self.http_status = http_status


class Requester:
    logger: Logger
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
    }

    def __init__(self, logger: Logger):
        self.logger = logger

    def get(self, url: str, allow_redirects: bool, timeout: int = 60) ->HttpResponse:
        try:
            response = requests.get(url, allow_redirects=allow_redirects, headers=self.headers, timeout=timeout)
        except MissingSchema:
            self.logger.LogMessage("ERROR", f"Invalid URL '{url}', perhaps you meant 'https://{url}'.")
            return HttpResponse(HttpResponseStatus.MissingSchema, None)
        except SSLError:
            self.logger.LogMessage("ERROR", f"Max retries exceeded with URL '{url}'.")
            self.logger.LogMessage("TIPS", "Let me have a rest.")
            self.logger.LogMessage("TIPS", "Crawl will continue after 20s.")
            time.sleep(20)
            return HttpResponse(HttpResponseStatus.MaxRetriesExceededWithUrl, None)
        except requests.exceptions.ConnectionError:
            self.logger.LogMessage("ERROR", "Internet error, maybe this error cause by VPN.")
            time.sleep(20)
            return HttpResponse(HttpResponseStatus.ConnectionError, None)
        else:
            if response.status_code == 200:
                self.logger.LogMessage("GET", f"{response.status_code}: {url}.")
                return HttpResponse(HttpResponseStatus.Success, response.content)
            elif response.status_code == 301:
                return HttpResponse(HttpResponseStatus.Redirects, response.content)
            elif response.status_code == 404:
                return HttpResponse(HttpResponseStatus.NoFound, response.content)
            else:
                self.logger.LogMessage("GET", f"{response.status_code}: {url}.")
                return HttpResponse(HttpResponseStatus.Invalid, response.content)


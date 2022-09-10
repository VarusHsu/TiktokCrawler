import openpyxl
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException
from openpyxl.worksheet.worksheet import Worksheet

from enums import XlsxWorkerStatus, XlsxReadStatus


class ReadResult:
    status: XlsxReadStatus
    url: str

    def __init__(self, status: XlsxReadStatus, url: str):
        self.status = status
        self.url = url


class XlsxWorker:
    status: XlsxWorkerStatus
    cur_line: int
    wb: Workbook
    ws: Worksheet

    def __init__(self):
        pass

    def read_url(self) -> ReadResult:
        if self.status != XlsxWorkerStatus.Reader:
            return ReadResult(XlsxReadStatus.PermissionDenied, "")
        value: str = self.ws.cell(self.cur_line, 1).value
        if value is None:
            return ReadResult(XlsxReadStatus.NoMoreData, "")
        else:
            self.cur_line += 1
            return ReadResult(XlsxReadStatus.Success, value)


def init_reader(path: str) -> XlsxWorker | None:
    instance = XlsxWorker()
    instance.status = XlsxWorkerStatus.Reader
    try:
        instance.wb = openpyxl.open(filename=path)
        instance.ws = instance.wb.worksheets[0]
    except InvalidFileException:
        return None
    instance.cur_line = 2
    return instance


def init_writer() -> XlsxWorker:
    pass

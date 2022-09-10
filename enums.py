from enum import Enum


class HttpResponseStatus(Enum):
    Invalid = 0
    MissingSchema = 1
    MaxRetriesExceededWithUrl = 2
    ConnectionError = 3
    Redirects = 4
    NoFound = 5
    Success = 6


class XlsxWorkerStatus(Enum):
    Invalid = 0
    Reader = 1
    Writer = 2


class XlsxReadStatus(Enum):
    Invalid = 0
    NoMoreData = 1
    PermissionDenied = 2
    Success = 3

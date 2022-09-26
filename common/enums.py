from enum import Enum


class HttpResponseStatus(Enum):
    Invalid = 0
    MissingSchema = 1
    MaxRetriesExceededWithUrl = 2
    ConnectionError = 3
    Redirects = 4
    NoFound = 5
    Success = 6
    Created = 7


class XlsxWorkerStatus(Enum):
    Invalid = 0
    Reader = 1
    Writer = 2
    RemoveDupReader = 3


class XlsxReadStatus(Enum):
    Invalid = 0
    NoMoreData = 1
    PermissionDenied = 2
    Success = 3


class XlsxWriteStatus(Enum):
    Invalid = 0
    NoSuchField = 1
    Success = 2
    PermissionDenied = 3


class UrlType(Enum):
    Invalid = 0
    VmTiktokCom = 1
    VtTiktokCom = 2
    WwwTiktokCom = 3
    WwwTiktokComT = 4
    KuaiVideoCom = 5
    SKwAiP = 6


class VideoResponseStatus(Enum):
    Invalid = 0
    Success = 1
    LoseEfficacy = 2
    BadUrlOrNoImplement = 3
    NetWorkError = 4
    ApiDataFormatError = 5
    MetaNotFound = 6


class GetHashtagInfoStatus(Enum):
    Invalid = 0
    Success = 1
    NetworkError = 2
    NoSuchHashtag = 3


class ListType(Enum):
    Invalid = 0
    ByTime = 1
    ByIncrease = 2


class XlsxCompareResult:
    Invalid = 0
    Uncompleted = 1
    YesterdayNotFound = 2
    TodayNotFound = 3
    YesterdayStatusException = 4
    TodayStatusException = 5
    BothTwoDaysException = 6
    Success = 7

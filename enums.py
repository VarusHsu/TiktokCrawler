from enum import Enum


class HttpResponseStatus(Enum):
    Invalid = 0
    MissingSchema = 1
    MaxRetriesExceededWithUrl = 2
    ConnectionError = 3
    Redirects = 4
    NoFound = 5
    Success = 6

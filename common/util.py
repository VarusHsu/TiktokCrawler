def merge_array(a: [], b: []) -> []:
    for item in b:
        if item not in a:
            a.append(item)
    return a


def replace_all(string: str, source: str, desc: str):
    res = ""
    sour_len = len(source)
    while True:
        index = string.find(source)
        if index == -1:
            break
        res += string[0:index] + desc
        string = string[index + sour_len:]
    res += string
    return res


def get_youtube_initialData(content: str) -> str:
    begin_index = content.find("InitialData = ") + len("InitialData = ")
    end_index = content.find(";", begin_index)
    res = content[begin_index:end_index]
    res = replace_all(res, "\\u", "\\\\u")
    res = replace_all(res, "\\x", "\\\\x")
    res = replace_all(res, "\\'", "\\\\'")
    res = replace_all(res, '\\\\"', "")
    return res

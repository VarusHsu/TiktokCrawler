def merge_array(a: [], b: []) -> []:
    for item in b:
        if item not in a:
            a.append(item)
    return a

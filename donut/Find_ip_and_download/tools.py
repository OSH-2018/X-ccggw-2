def dict_add(dic: dict, key):
    if dic.__contains__(key) and isinstance(dic[key], int):
        dic[key] += 1
    elif not dic.__contains__(key):
        dic[key] = 1
    else:
        raise TypeError
content = ""


def extract_frost(content):
    frost_dic = {}
    if content.find("霜") != -1 and content.find("结束") != -1:
        frost_dic["霜结束"] = 1
    else:
        if content.find("霜") != -1:
            frost_dic["霜出现"] = 1
    return frost_dic
import re

content = "  天津机场降雪天气已经结束，过程降雪量0.8毫米，积雪深度0厘米，取消03：33发布的机场警报（降雪）。"


def Normalize(sentence):
    sentence = sentence.replace("公里", "千米").replace("km", "千米")
    sentence = sentence.replace('m', '米')
    sentence = sentence.replace("cm", "厘米").replace("公分", "厘米")
    sentence = sentence.replace("mm", "毫米").replace('~', '-')
    return sentence


def IsDigit(char):
    if char.isdigit() or char == '*' or char == '-':
        return True
    else:
        return False


def extract_digit(sentence, keyword, unit):
    digit = ''
    if keyword == '':
        flag = sentence.find(unit)
        flag -= 1
        while flag >= 0:
            if IsDigit(sentence[flag]):
                digit = sentence[flag] + digit
            else:
                break
            flag -= 1
    else:
        flag1 = sentence.find(keyword)
        flag2 = sentence[flag1:].find(unit)
        reminder = 0
        for i in range(flag1, flag2 + flag1):
            if IsDigit(sentence[i]):
                reminder = 1
                digit += sentence[i]
            if not IsDigit(sentence[i]) and reminder == 1:
                break
    return digit


def extract_snow_fall(sentences, snow_dic, keyword):
    snow_dic[keyword + "天气"] = 1
    for sentence in sentences:
        if keyword in sentence:
            if "结束" in sentence:
                snow_dic[keyword + "天气"] = 0
            if "无" + keyword in sentence:
                snow_dic[keyword + "天气"] = 0
            if "未出现" in sentence:
                snow_dic[keyword + "天气"] = 0
            if "不会产生" in sentence:
                snow_dic[keyword + "天气"] = 0
    return snow_dic


def extract_snow_detail(sentences, snow_dic):
    for sentence in sentences:
        if "雪" in sentence and "融雪" not in sentence and "积雪" not in sentence:
            items = re.findall('(维持|持续|连续性|短时|间歇性.*?)*([大中小]*到*[大中小]*)(阵*)(雨夹)*(雪|雨)转*(维持|持续|连续性|短时|间歇性.*?)*([大中小]*到*[大中小]*)(阵*)(雨夹)*(雪|雨)*', sentence)
            items = items[0]
            snow_dic["时间特性"] = items[0]
            snow_dic["强度"] = items[1]
            snow_dic["到强度"] = items[2]
            if items[3] == "雨夹":
                snow_dic["是否雨夹雪"] = 1
                snow_dic["转前天气"] = "雨夹雪"
            if "转前天气" not in snow_dic:
                snow_dic["转前天气"] = items[4]
            if "转" in sentence:
                snow_dic['转后时间特性'] = items[5]
                snow_dic["转后强度"] = items[6]
                snow_dic["转后到强度"] = items[7]
                if items[8] == "雨夹":
                    snow_dic["转后是否雨夹雪"] = 1
                    snow_dic["转后天气"] = "雨夹雪"
                if "转后天气" not in snow_dic:
                    snow_dic["转后天气"] = items[9]
    return snow_dic


def extract_snow(content):
    snow_dic = {}
    snow_dic["降雪天气"] = 0
    sentences = content.split('，')
    if "雪" in content:
        snow_dic = extract_snow_fall(sentences, snow_dic, "降雪")
    if snow_dic["降雪天气"] == 1:
        snow_dic = extract_snow_detail(sentences, snow_dic)
    if "融雪" in content:
        snow_dic = extract_snow_fall(sentences, snow_dic, "融雪")
    if "积雪" in content:
        snow_dic = extract_snow_fall(sentences, snow_dic, "积雪")
    if "积冰" in content:
        snow_dic = extract_snow_fall(sentences, snow_dic, "积冰")
    for sentence in sentences:
        sentence  = Normalize(sentence)
        if "积雪" in sentence:
            snow_depth = extract_digit(sentence, "积雪", "厘米")
            if snow_depth != "":
                snow_dic["积雪深度"] = snow_depth + "厘米"
            else:
                snow_depth = extract_digit(sentence, "积雪", "毫米")
                if snow_depth != '':
                    snow_dic["积雪深度"] = snow_depth + "毫米"
    for key, value in snow_dic.items():
        if value == '':
            snow_dic[key] = 'Null'
    return snow_dic
    #print(snow_dic)


extract_snow(content)
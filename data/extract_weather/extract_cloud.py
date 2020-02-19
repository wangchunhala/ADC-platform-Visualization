import re

content = " 在浦东机场西部及北部有对流云团发展，对流云团顶高9-10公里，以40公里/小时向偏东移动，强度不变"

strength = ["强的", "弱的", "中等"]
shape = ["成片", "分散", '块状', '带状', '孤立']
type = ["对流云", "雷暴云", "雷雨云", '降水云']


def extract_location(sentence, cloud_dic):
    sentence = Normalize(sentence)
    info = re.findall(
        '[机|本]场(东南|西北|东北|西南|附近|东|西|南|北)[方面侧部]*(距离|处)*(.*?)千米.*云团',
        sentence)
    if info != []:
        info = info[0]
        cloud_dic["位置方向"] = "机场" + info[0]
        if info[2] != '':
            cloud_dic["云团距离"] = info[2] + '千米'
    else:
        info = re.findall(
            '[机|本]场(.*?)有.* [发展|移]', sentence)
        if info != []:
            cloud_dic["位置方向"] = "机场" + info[0]
    return cloud_dic


def IsDigit(char):
    if char.isdigit() or char == '*' or char == '-' or char == '米':
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
        if flag2 != -1:
            start = flag1
            end = flag1 + flag2
            reminder = 0
            for i in range(start, end):
                if IsDigit(sentence[i]):
                    reminder = 1
                    digit += sentence[i]
                if (not IsDigit(sentence[i])) and reminder == 1:
                    break
        else:
            flag2 = sentence[:flag1].find(unit)
            index = flag2 - 1
            while index >= 0:
                if IsDigit(sentence[index]):
                    digit = sentence[index] + digit
                else:
                    break
                index -= 1
    return digit

keyword_list = ["顶高", "范围", "东西向", "南北向", "西北东南向", "东北西南向", "东南西北向", "西南东北向", '宽']
direction = ["东", "西", "南", "北", "偏", "方", "向"]
strength_alter = ["减弱", "增强", "维持", "不变", '加强']
scope_dir = ["东西向", "南北向", "西北东南向", "东北西南向", "东南西北向", "西南东北向"]


def Normalize(sentence):
    sentence = sentence.replace("公里", "千米").replace("km", "千米").replace('KM', '千米')
    sentence = sentence.replace('m', '米').replace('~', '-').replace('--', '-')
    for i in range(len(sentence)):
        if sentence[i] == '-':
            if sentence[i-2:i] == '千米':
                sentence = sentence[:i-2] + '@@' + sentence[i:]
            if sentence[i-1] == '米':
                sentence = sentence[:i-1] + '@' + sentence[i:]
    sentence = sentence.replace('@', '')
    return sentence


def extract_direction(sentence):
    dir = ''
    flag = sentence.find("移动")
    flag -= 1
    reminder = 0
    while flag >= 0:
        if sentence[flag] in direction:
            dir = sentence[flag] + dir
            reminder = 1
        if sentence[flag] not in direction and reminder == 1:
            break
        flag -= 1
    if "移出本场" in sentence:
        dir = "移出本场"
    if dir == '':
        raw_dir = re.findall('([东西南北])移', sentence)
        if raw_dir != []:
            dir = '向' + raw_dir[0]
    return dir


def extract_cloud_cluster(sentences, cloud_dic):
    cloud_dic["有云团或云系"] = 1
    for sentence in sentences:
        sentence = Normalize(sentence)
        if sentence.find('云团') != -1 or sentence.find('云系') != -1:
            for strength_level in strength:
                if sentence.find(strength_level) != -1:
                    cloud_dic["云强度"] = strength_level
            for tp in type:
                if sentence.find(tp) != -1:
                    cloud_dic["云类型"] = tp + '团'
        for shape_type in shape:
            if sentence.find(shape_type) != -1:
                cloud_dic["云形态"] = shape_type
        for keyword in keyword_list:
            if sentence.find(keyword) != -1:
                digit = extract_digit(sentence, keyword, '千米')
                cloud_dic[keyword] = digit + '千米'
        if sentence.find('千米/小时') != -1:
            digit = extract_digit(sentence, '', "千米/小时")
            cloud_dic["移动速度"] = digit + '千米/小时'
        if sentence.find('移') != -1:
            dir = extract_direction(sentence)
            cloud_dic["移动方向"] = dir
        if sentence.find("强度") != -1 or sentence.find("云") != -1:
            for alter_type in strength_alter:
                if sentence.find(alter_type) != -1:
                    cloud_dic['强度变化'] = alter_type
                    break
    return cloud_dic


def extract_low_cloud(sentences, cloud_dic):
    cloud_dic["有低云天气"] = 1
    for sentence in sentences:
        sentence = Normalize(sentence)
        cloud_btm = re.findall('云底高(.*?)（(.*?)）', sentence)
        if len(cloud_btm) > 0 and len(cloud_btm[0]) == 2:
            cloud_btm = cloud_btm[0]
            cloud_dic["云底高"] = cloud_btm[0]
            cloud_dic["低云量级"] = cloud_btm[1]
        else:
            if '云底高' in sentence or '低云' in sentence:
                if '云底高' in sentence:
                    digit = extract_digit(sentence, "云底高", "米")
                else:
                    digit = extract_digit(sentence, "", "米")
                cloud_dic["云底高"] = digit + '米'
                if "量级" in sentence:
                    magnitude = re.findall("（(.*?)）", sentence)[0]
                    cloud_dic["低云量级"] = magnitude
        temp_info = re.findall('短时(.*)（(.*)）', sentence)
        if len(temp_info) > 0 and len(temp_info[0]) == 2:
            temp_info = temp_info[0]
            cloud_dic["短时云底高"] = temp_info[0]
            cloud_dic["短时低云量级"] = temp_info[1]
    return cloud_dic


def scope_refine(dir, dic):
    if dir in dic:
        dic[dir + "范围"] = dic[dir]
        dic.__delitem__(dir)
        try:
            dic.__delitem__("范围")
        except:
            pass
    return dic


def final_refine(cloud_dic):
    if '范围' in cloud_dic and cloud_dic['范围'] == '千米':
        cloud_dic.__delitem__('范围')
    if '宽' in cloud_dic:
        cloud_dic['云团宽度'] = cloud_dic['宽']
        cloud_dic.__delitem__('宽')
    return cloud_dic


def extract_cloud(content):
    cloud_dic = {}
    cloud_dic["云团/系与回波信息"] = 0
    cloud_dic["低云天气信息"] = 0
    content = content.replace('对流云', '对流云团').replace(',', '，').replace('回波', '云团')
    sentences = content.split('，')
    if content.find('云团') != -1 or content.find('云系') != -1:
        cloud_dic = extract_cloud_cluster(sentences, cloud_dic)
    if content.find('低云') != -1 or content.find('云底') != -1:
        cloud_dic = extract_low_cloud(sentences, cloud_dic)
    for scp_dir in scope_dir:
        cloud_dic = scope_refine(scp_dir, cloud_dic)
    cloud_dic = extract_location(content, cloud_dic)
    cloud_dic = final_refine(cloud_dic)
    return cloud_dic


extract_cloud(content)

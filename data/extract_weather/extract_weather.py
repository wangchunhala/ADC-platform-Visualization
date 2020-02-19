from data.extract_weather.extract_snow import extract_snow
from data.extract_weather.extract_cloud import extract_cloud
from data.extract_weather.xuan import subsentence_seg, extract_rain, extract_yuji
from data.extract_weather.xinyi import extract_cancel, vis, wind
from data.extract_weather.extract_frost import extract_frost


def extract_influence(content, dic):
    sentences = content.split('，')
    target_sentence = sentences[0]
    if target_sentence.find("受") != -1 and target_sentence.find("影响") != -1:
        dic["影响原因"] = target_sentence
        if sentences[1].find("预计") != -1:
            dic["影响目前或未来"] = "未来"
        else:
            dic["影响目前或未来"] = "目前"
    return dic


def extract_present(content):
    end_list = ['解除', '取消', '预计']
    content = content.replace("取消", "，取消").replace("，，取消", "，取消")
    content = content.replace("预计", "，预计").replace("，，预计", "，预计")
    sentences = content.split('，')
    flag = 0
    for word in end_list:
        if sentences[0].find(word) != -1:
            flag = 1
            break
    if flag == 0:
        subcontent = ''
        for sentence in sentences:
            flag2 = 0
            for word in end_list:
                if sentence.find(word) != -1:
                    flag2 = 1
                    break
            if flag2 == 1:
                break
            else:
                subcontent += (sentence + '，')
        return subcontent.replace(' ', '').replace('\t', '')
    else:
        return ''


def parse_sentence(sentence):
    cloud_dic = extract_cloud(sentence)
    vis_dic = vis(sentence)
    wind_dic = wind(sentence)
    snow_dic = extract_snow(sentence)
    rain_dic = {}
    rain = extract_rain(sentence)
    if rain[0] != 'Null':
        rain_dic["雨类型"] = rain[0]
    if rain[1] != 'Null':
        rain_dic["雨强度"] = rain[1]
    frost_dic = extract_frost(sentence)
    thunder_dic = {}
    if "闻雷" in sentence:
        thunder_dic["机场闻雷"] = 1
    if "干雷暴" in sentence:
        thunder_dic["干雷暴"] = 1
    else:
        if '雷暴' in sentence:
            thunder_dic["雷暴"] = 1
    return cloud_dic, vis_dic, wind_dic, snow_dic, rain_dic, frost_dic, thunder_dic


def construct_info_list(sentence_list):
    info_list = []
    for sentence in sentence_list:
        current_dic = {}
        current_dic["时间槽"] = sentence[0]
        current_sentence = sentence[1]
        cloud_dic, vis_dic, wind_dic, snow_dic, rain_dic, frost_dic, thunder_dic = parse_sentence(current_sentence)
        current_dic["云天气"] = cloud_dic
        current_dic["能见度"] = vis_dic
        current_dic["风天气"] = wind_dic
        current_dic["雨天气"] = rain_dic
        current_dic["雪天气"] = snow_dic
        current_dic["霜天气"] = frost_dic
        current_dic["雷天气"] = thunder_dic
        info_list.append(current_dic)
    return info_list

def PrintOut(dic):
    print("=========================影响原因分析===========================")
    if "影响原因" in dic:
        print("影响原因：" + dic["影响原因"])
        print("影响目前或未来：" + dic["影响目前或未来"])
    else:
        print('无相关内容')
    print("=========================目前天气信息===========================")
    present_info_list = dic["目前天气信息"]
    for item in present_info_list:
        print("【" + item["时间槽"] + '】')
        for key, value in item.items():
            if key == "时间槽":
                continue
            print("\t*****" + key + "*****")
            print("\t\t", value)
    print("=========================预计天气信息===========================")
    present_info_list = dic["预计天气信息"]
    for item in present_info_list:
        print("【" + item["时间槽"] + '】')
        for key, value in item.items():
            if key == "时间槽":
                continue
            print("\t*****" + key + "*****")
            print("\t\t", value)
    print("=========================取消信息相关===========================")
    print("取消报文所指时间", dic["取消报文所指时间"])
    print("取消报文告警原因", dic["取消报文告警原因"])
    print("取消报文号码", dic["取消报文号码"])

def work(content):
    dic = {}
    # key: 影响系列：影响原因，影响目前或未来；取消系列：取消报文所指时间，取消报文告警原因，取消报文号码；
    dic = extract_influence(content, dic) # 提取天气影响原因
    present = extract_present(content) # 提取目前天气
    cancel = extract_cancel(content) # 提取取消告警信息
    future = ''
    if "预计" in content:
        future = extract_yuji(content) # 提取预计信息
    # about cancel
    dic["取消报文所指时间"] = cancel["时间"]
    dic["取消报文告警原因"] = cancel["原因"]
    dic["取消报文号码"] = cancel["号码"]
    # about present
    sentence_list = subsentence_seg(present)
    if sentence_list == []:
        sentence_list = [["目前", present]]
    present_info_list = construct_info_list(sentence_list)
    dic["目前天气信息"] = present_info_list
    # about future
    sentence_list = subsentence_seg(future)
    future_info_list = construct_info_list(sentence_list)
    dic["预计天气信息"] = future_info_list


    return dic
# content = "预计北京时间20日01:00 - 20日09:00石家庄正定机场能见度低于500米。 "
# work(content)
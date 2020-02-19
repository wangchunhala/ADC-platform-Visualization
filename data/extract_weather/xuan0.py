# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 09:26:07 2019

@author: xuanw
"""

import jieba
import jieba.analyse
import jieba.posseg

import re
import string

'''
添加特殊标记的词
'''
jieba.add_word('北京时间',tag='time_type')

jieba.add_word('长沙机场',tag='airport_type')
jieba.add_word('武汉机场',tag='airport_type')
jieba.add_word('虹桥机场',tag='airport_type')
jieba.add_word('正定机场',tag='airport_type')

jieba.add_word('雷暴',tag='thunder_type') 
jieba.add_word('干雷暴',tag='thunder_type') 

jieba.add_word('小到中雨',tag='rain_type')
jieba.add_word('中到大雨',tag='rain_type') 
jieba.add_word('阵雨',tag='rain_type')
jieba.add_word('雷雨',tag='rain_type') 
jieba.add_word('雷阵雨',tag='rain_type') 
jieba.add_word('小雨',tag='rain_type') 
jieba.add_word('中雨',tag='rain_type') 
jieba.add_word('大雨',tag='rain_type')
jieba.add_word('阵型降水',tag='rain_type')

jieba.add_word('强降水',tag='rain_state') 
jieba.add_word('弱降水',tag='rain_state')

jieba.add_word('中等强度',tag='b') 
jieba.add_word('小到中',tag='b')
jieba.add_word('中到大',tag='b')
jieba.add_word('中-大',tag='b')
jieba.add_word('强',tag='b')


def sentence_seg(sentence):
    '''
    带词性标注，对句子进行分词，不排除停词等
    :param sentence:输入字符
    :return:
    '''
    sentence_seged = jieba.posseg.cut(sentence.strip())
    outstr = ''
    for x in sentence_seged:
        outstr+="{}/{};".format(x.word,x.flag)
        
    return outstr


def sentence_proc(sstring):
    '''
    处理句子，将句子变成string序列
    :param sstring:输入字符
    :return:
    '''
    outstr = sstring.split(';')
    return outstr[0:len(outstr)-1]


def extract_rain(sentence):
    '''
    抽取雨类
    :param sentence:输入句子
    :return:
    '''
    rain = 'Null'
    airport = 'Null'
    rainstate = 'Null'

    if '-' in sentence:
        sentence = sentence.replace('-', '到')
    sent_string = sentence_seg(sentence)
    sent_list = sentence_proc(sent_string)

    for i in range(len(sent_list)):
        if 'rain_type' in sent_list[i]:
            rain = sent_list[i].split('/')[0]
        if 'rain_state' in sent_list[i]:
            rainstate = sent_list[i].split('/')[0]       
        if 'airport_type' in sent_list[i]:
            airport = sent_list[i].split('/')[0]
    
        if 'rain_type' in sent_list[i]:
            if 'a' in sent_list[i-1] or 'b' in sent_list[i-1]:
                if len(rainstate) > 0 :
                    rainstate = sent_list[i-1].split('/')[0]
                else:
                    rainstate += sent_list[i-1].split('/')[0]
            
    return rain, rainstate, airport


def extract_time(sentence):
    '''
    抽取时间
    :param sentence:输入句子
    :return:
    '''
    match_time = []
    start_time = []
    end_time = []

    sentence = re.sub('\s', '', sentence)
    if '~' in sentence:
        sentence = sentence.replace('~', '-')
    if '--' in sentence:
        sentence = sentence.replace('--', '-')
    if '到' in sentence:
        sentence = sentence.replace('到', '-')
    if '至' in sentence:
        sentence = sentence.replace('至', '-')

    sent_string = sentence_seg(sentence)
    sent_list = sentence_proc(sent_string)

    for i in range(len(sent_list)):
        if 'time_type' in sent_list[i]:
            time = sent_list[i].split('/')[0]
            start = ''
            end = ''
            j = 1
            while j < len(sent_list) - i:
                if ('m' in sent_list[i + j] or '-' in sent_list[i + j] or '时' in sent_list[i + j]):
                    time += sent_list[i + j].split('/')[0]
                    start = i
                    end = i + j
                    j += 1
                else:
                    break
            match_time.append(time)
            start_time.append(start)
            end_time.append(end)
        if '月' in sent_list[i]:
            if end_time != [] and i > int(max(end_time)):
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = ''
                end = ''
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
            elif end_time == []:
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = ''
                end = ''
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
        if '日' in sent_list[i]:
            if end_time != [] and i > int(max(end_time)):
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = ''
                end = ''
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
            elif end_time == []:
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = ''
                end = ''
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
        if (':' in sent_list[i] or '：' in sent_list[i]) and ('m' in sent_list[i - 1]):
            if end_time != [] and i > int(max(end_time)):
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = ''
                end = ''
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
            elif end_time == []:
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = ''
                end = ''
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
        if '时' in sent_list[i] and ('m' in sent_list[i - 1]):
            if end_time != [] and i > int(max(end_time)):
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = i - 1
                end = i
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)
            elif end_time == []:
                time = sent_list[i - 1].split('/')[0]
                time += sent_list[i].split('/')[0]
                start = i - 1
                end = i
                j = 1
                while j < len(sent_list) - i:
                    if ('m' in sent_list[i + j] or 'x' in sent_list[i + j] or '时' in sent_list[i + j]):
                        time += sent_list[i + j].split('/')[0]
                        start = i - 1
                        end = i + j
                        j += 1
                    else:
                        break
                match_time.append(time)
                start_time.append(start)
                end_time.append(end)

    return match_time, start_time, end_time

def subsentence_seg(sentence):
    '''
    按照时间出现次数切分句子
    :param sentence:输入句子
    :return:
    '''
    sent_string = sentence_seg(sentence)
    sent_list = sentence_proc(sent_string)

    sub_sentence = list()

    ttime, stime, etime = extract_time(sentence)
    stime.append(len(sent_list))

    if ttime != []:
        for i in range(len(ttime)):
            sent = []
            for j in range(etime[i] + 1, stime[i + 1]):
                sent.append(sent_list[j].split('/')[0])
            subsent = ''.join(sent)
            sub_sentence.append([ttime[i], subsent])

    ssent = []
    for i in range(len(sub_sentence)):
        ssent.append(sub_sentence[i][0])
        ssent.append(sub_sentence[i][1])

    return ssent


#sentence = "哈尔滨机场目前已出现小雪天气，主导能见度3500米，预计20日21时至23时有小雨夹雪，能见度1~4公里；20日23时至21日14时为连续性小雪，能见度1~4公里，期间21日02时~10时有短时中阵雪，能见度最低约600米。降雪期间地面风向为东北风，风向350-050度，平均风速4~8米/秒，阵风10~13米/秒，温度-9~0℃。请相关部门注意20日23时之前地面融雪的不利影响，同时关注跑道积雪结冰和航空器空中积冰"
#sent_lists = subsentence_seg(sentence)

#for slist in sent_lists:
#    print(extract_rain(slist[1]),slist[0])
    

def extract_yuji(sentence):
   '''
   抽取句子中的预计成份
   :param sentence:输入句子
   :return:
   '''    
   seg_list = jieba.cut(sentence)
   segment_ci = " ".join(seg_list)
   segment_ci = segment_ci.split()    
   
   location_yuji = -1
   location_quxiao = -1
   outsent = ''
   
   if '预计' in sentence:
       location_yuji = segment_ci.index('预计')    
   if '取消' in sentence:
       location_quxiao = segment_ci.index('取消') 
   if '解除' in sentence:
       location_quxiao = segment_ci.index('解除') 
   
   if location_yuji != -1 and location_quxiao != -1:
       outsent = segment_ci[location_yuji:location_quxiao]
       outsent = ''.join(outsent)
   if location_yuji != -1 and location_quxiao == -1:
       outsent = segment_ci[location_yuji:-1]
       outsent = ''.join(outsent)
   
   return outsent
   
#print(sentence)
#print(extract_yuji(sentence))
# -*- coding: utf-8 -*-
"""
Created on Fri May 10 08:59:03 2019

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

sentence = "在长沙机场西南面60公里处有强的成片对流云团，范围60*120km，云团顶高8-11公里，以50公里/小时的速度向东偏北移动，强度不变，预计北京时间21日09:10 - 21日10:10影响长沙机场并出现雷暴天气。13时其间长沙机场还将出现中-大阵型降水，短时13-17m/s阵风，低空风切变等伴随天气。"

def extract_time(sentence):
    '''
    抽取时间
    :param sentence:输入句子
    :return:
    '''
    match_time = []
    start_time = []
    end_time = []
    
    sentence = re.sub('\s','',sentence)
    if '~' in sentence:
        sentence = sentence.replace('~','-')
    if '--' in sentence:
        sentence = sentence.replace('--','-')
    if '到' in sentence:
        sentence = sentence.replace('到','-') 
    if '至' in sentence:
        sentence = sentence.replace('至','-')          

    sent_string = sentence_seg(sentence)
    sent_list = sentence_proc(sent_string)    

    for i in range(len(sent_list)):
       if 'time_type' in sent_list[i]:
           time = sent_list[i].split('/')[0]
           start = ''
           end = ''
           j = 1 
           while j < len(sent_list):
               if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                   time += sent_list[i+j].split('/')[0]
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
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = ''
               end = ''           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end)
           elif end_time == []:
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = ''
               end = ''           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
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
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = ''
               end = ''           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end)              
           elif end_time == []:
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = ''
               end = ''           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end) 
       if (':' in sent_list[i] or '：' in sent_list[i]) and ('m' in sent_list[i-1]):
           if end_time != [] and i > int(max(end_time)):
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = ''
               end = ''           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end)              
           elif end_time == []:
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = ''
               end = ''           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end) 
       if '时' in sent_list[i] and ('m' in sent_list[i-1]):
           if end_time != [] and i > int(max(end_time)):
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = i - 1
               end = i            
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end)              
           elif end_time == []:
               time = sent_list[i-1].split('/')[0]
               time += sent_list[i].split('/')[0]
               start = i - 1
               end = i           
               j = 1 
               while j < len(sent_list):
                   if ('m' in sent_list[i+j] or 'x' in sent_list[i+j] or '时' in sent_list[i+j]):
                       time += sent_list[i+j].split('/')[0]
                       start = i - 1
                       end = i + j
                       j += 1
                   else:
                       break 
               match_time.append(time)     
               start_time.append(start)  
               end_time.append(end) 
   
    return match_time,start_time,end_time

def subsentence_seg(sentence):    
    '''
    按照时间出现次数切分句子
    :param sentence:输入句子
    :return:
    '''    
    sent_string = sentence_seg(sentence)
    sent_list = sentence_proc(sent_string)

    sub_sentence = list()

    ttime,stime,etime = extract_time(sentence) 
    stime.append(len(sent_list))
    
    if ttime != []:
        for i in range(len(ttime)):
            sent = []
            for j in range(etime[i]+3,stime[i+1]):
                sent.append(sent_list[j].split('/')[0])
            subsent = ''.join(sent)            
            sub_sentence.append([ttime[i],subsent])   

    ssent = []
    for i in range(len(sub_sentence)):
        ssent.append([sub_sentence[i][0],sub_sentence[i][1]])
        
    return ssent

sentence_list = subsentence_seg(sentence)






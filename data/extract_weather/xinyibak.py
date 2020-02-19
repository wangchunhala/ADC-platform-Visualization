# -*- coding: utf-8 -*-

import re
import string

#取消／解除:时间(日,时,分),几号警报，警报原因(末尾括号中内容)

def cancel_time(sstring):
        if '取消' not in sstring and '解除' not in sstring:
                return 'null'
        if '解除' in sstring:
                sstring = sstring.replace('解除','取消')
        if '取消' in sstring:
                match_location = re.search('取消',sstring).span()
                answer_sstring = sstring[match_location[0]:]
                answer_list=['xx','xx','xx']
                if '日' in answer_sstring:
                        match_location1 = re.search('日',answer_sstring).span()
                        day = ''
                        begin = match_location1[0]-1
                        s = answer_sstring[begin]
                        while s.isdigit():
                                begin = begin-1
                                day = s+day
                                s = answer_sstring[begin]
                        answer_list[0]=day
                if '：' in answer_sstring:
                        match_location2 = re.search('：',answer_sstring).span()
                        if answer_sstring[match_location2[0]-1].isdigit():
                                answer_sstring = answer_sstring.replace('：',':')
                if ':' in answer_sstring:
                        match_location2 = re.search(':',answer_sstring).span()
                        begin = match_location2[0]
                        answer_list[1] = answer_sstring[begin-2:begin]
                        
                        answer_list[2] = answer_sstring[begin+1:begin+3]
                return answer_list[0]+':'+answer_list[1]+':'+answer_list[2]

        return 'null'       



def cancel_number(sstring):
        if '取消' not in sstring and '解除' not in sstring:
                return 'null'
        if '解除' in sstring:
                sstring = sstring.replace('解除','取消')
        if '取消' in sstring:
                match_location = re.search('取消',sstring).span()
                answer_sstring = sstring[match_location[0]:]
                if '号' in answer_sstring:
                        match_location1 = re.search('号',answer_sstring).span()
                        number = ''
                        begin = match_location1[0]-1
                        s = answer_sstring[begin]
                        while s.isdigit():
                                begin = begin-1
                                number = s+number
                                s = answer_sstring[begin]
                        return number
        return 'null'


def cancel_reason(sstring):
        if '取消' not in sstring and '解除' not in sstring:
                return 'null'
        if '解除' in sstring:
                sstring = sstring.replace('解除','取消')
        if '取消' in sstring:
                match_location = re.search('取消',sstring).span()
                answer_sstring = sstring[match_location[0]:]
                if '（' in answer_sstring:
                        answer_sstring = answer_sstring.replace('（','b')
                        answer_sstring = answer_sstring.replace('）','e')
                if 'b' in answer_sstring and 'e' in answer_sstring:
                        begin = re.search('b',answer_sstring).span()
                        end = re.search('e',answer_sstring).span()
                        return answer_sstring[begin[1]:end[0]]
        return 'null'


#预计:时间(日,时,分)(一般有几点到几点的标记),哪个机场，发生什么事，是否是持续


#能见度判断：1.能见度xx米／公里（公里换成米*1000） xx-xx米 xx-xx公里 2.最低 3. 是否有浮尘 4.RVR xx米
#是否有浮尘
def vis_dust(sstring):
        if '浮尘' in sstring:
                return '浮尘'
        else:
                return 'null'
#返回 [(xx,xx)多少米至多少米，如果是只有一个就两个填一样的eg:500-500]
#keyword分4种，垂直能见度，最低能见度，RVR能见度，普通能见度

def vis_distance(keyword,sstring):
        if keyword not in sstring:
                return 'null'
        answer_list = []
        sstring = sstring.split('，')
        
        index = 0
        for index in range(len(sstring)):
                if keyword in sstring[index]:
                        flag = '米'#要不要把公里变成米
                        if '度' not in keyword and '度' in sstring[index]:
                                flag = '度'
                                sstring[index] = sstring[index].replace('至','-')
                                match_location1 = re.search('度',sstring[index]).span()
                                sstring[index] = sstring[index][:match_location1[0]]
                                answer = ''
                                
                                for i in range(len(sstring[index])):
                                        s = sstring[index][len(sstring[index])-i-1]
                                        if s.isdigit() or s=='-' or s =='~':
                                                
                                                answer = s+answer
                                        else:
                                                break
                                if answer[0]=='-' or answer[0]=='~':
                                        answer=answer[1:]
                                if answer!='':
                                        answer_list.append([flag,answer])
                        if 'm/s' not in keyword and'm/s' in sstring[index]:
                                sstring[index] = sstring[index].replace('m/s','米/秒')
                        if '米/秒' not in keyword and'米/秒' in sstring[index]:
                                flag = '米/秒'
                                sstring[index] = sstring[index].replace('至','-')
                                match_location1 = re.search('米/秒',sstring[index]).span()
                                sstring[index] = sstring[index][:match_location1[0]]
                                answer = ''
                                
                                for i in range(len(sstring[index])):
                                        s = sstring[index][len(sstring[index])-i-1]
                                        if s.isdigit() or s=='-' or s =='~':
                                                
                                                answer = s+answer
                                        else:
                                                break
                                if answer[0]=='-' or answer[0]=='~':
                                        answer=answer[1:]
                                if answer!='':
                                        answer_list.append([flag,answer])
                        if '公里' not in keyword and'公里' in sstring[index]:
                                flag = '公里'
                                sstring[index] = sstring[index].replace('公里','米')
                        if 'km' not in keyword and'km' in sstring[index]:
                                flag = 'km'
                                sstring[index] = sstring[index].replace('km','米')
                        if '米' not in keyword and'米' in sstring[index]:

                                match_location1 = re.search('米',sstring[index]).span()
                                sstring[index] = sstring[index][:match_location1[0]]
                                answer = ''

                                for i in range(len(sstring[index])):
                                        
                                        s = sstring[index][len(sstring[index])-i-1]
                                        
                                        if s.isdigit() or s=='-' or s =='~':
                                                
                                                answer = s+answer
                                        else:
                                                break
                                if answer[0]=='-' or answer[0]=='~':
                                        answer=answer[1:]
                                if answer!='':
                                        answer_list.append([flag,answer])
                


        return answer_list

#返回最低能见度多少米['xx','xx']
def vis_low(sstring):
        if '最低能见度' in sstring:
                return vis_distance('最低能见度',sstring)
        if '能见度最低' in sstring:
                return vis_distance('能见度最低',sstring)
        return 'null'

#返回句子中所有RVR后面跟随的距离['xx','xx'...]
def vis_RVR(sstring):
        if 'RVR' in sstring:
                return vis_distance('RVR',sstring)
        return 'null'

#返回垂直能见度后面的距离
def vis_verti(sstring):
        if '垂直能见度' in sstring:
                return vis_distance('垂直能见度',sstring)
        return 'null'

def vis_wu(sstring):
        if '雾' in sstring:
                return '雾'
        else:
                return 'null'

#风 判断：1 方向 东西南北 2平均风速 xxm/s 3 阵风（也是风速）xx米／秒 4 xx级 风 5 风向 xx度-xx度 xx-xx度 6 风切变／低空风切变 7颠簸

def wind_dianbo(sstring):
        if '颠簸' in sstring:
                return '颠簸'
        else:
                return 'null'
def wind_qiebian(sstring):
        if '低空风切变' in sstring:
                return '低空风切变'
        if '风切变'  in sstring:
                return '风切变'
        return 'null'

def wind_direction(sstring):
        if '风' not in sstring:
                return 'null'
        answer = ''
        word_list = ['东','南','西','北','偏']
        
        candidate_sstring = sstring
        begin = 0 
        while answer =='' and '风' in candidate_sstring:
                match_location = re.search('风',candidate_sstring).span()
                
                begin = match_location[1]
                find = match_location[1]-1
                flag = -1
                for i in range(5) :
                        
                        if find-i>=0 and candidate_sstring[find-i] in word_list:
                                flag = find-i
                                break

                if flag!=-1:
                        while flag>=0 and candidate_sstring[flag] in word_list:
                                answer = candidate_sstring[flag]+answer
                                flag = flag-1
                candidate_sstring = candidate_sstring[begin:]
        return answer

def wind_avg(sstring):
        if '平均风速' in sstring:
                return vis_distance('平均风速',sstring)
        if '平均风' in sstring:
                return vis_distance('平均风',sstring)
        return 'null'

def wind_zf(sstring):
        if '阵风' in sstring:
                return vis_distance('阵风',sstring)
        return 'null'

def wind_direction2(sstring):
        if '风向' in sstring:
                return vis_distance('风向',sstring)
        return 'null'

test = "目前本场能见度1400米，RVR2000米，解除大雾机场警报。 "


def wind(sstring):
        dict_wind={}
        dict_wind['颠簸']= wind_dianbo(sstring)
        dict_wind['风切变']=wind_qiebian(sstring)
        dict_wind['方位方向']=wind_direction(sstring)
        dict_wind['数字方向']=wind_direction2(sstring)
        dict_wind['平均风速']=wind_avg(sstring)
        dict_wind['阵风风速']=wind_zf(sstring)
        return dict_wind
def vis(sstring):
        dict_vis={}
        dict_vis['浮尘']=vis_dust(sstring)
        dict_vis['雾']=vis_wu(sstring)
        dict_vis['最低能见度']=vis_low(sstring)
        dict_vis['RVR']=vis_RVR(sstring)
        dict_vis['垂直能见度']=vis_verti(sstring)
        dict_vis['普通能见度']='null'
        if vis_low(sstring) == 'null' and vis_verti(sstring) == 'null' and '能见度' in sstring:
                dict_vis['common'] = vis_distance('能见度',sstring)
        return dict_vis

def cancel(sstring):
        dict_cancel={}
        dict_cancel['时间']=cancel_time(sstring)
        dict_cancel['号码']=cancel_number(sstring)
        dict_cancel['原因']=cancel_reason(sstring)
        return dict_cancel


print (vis(test))































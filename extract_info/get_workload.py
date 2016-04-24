#!/usr/bin/python2.7 -tt
# -*- coding: UTF-8 -*-
import re,os,time
'''
代码使用介绍：
python版本为2.7.11，采用的编译器为Anconda2
算法介绍：
首先将换行不规则的文档全部转化为一行，查找出所有‘x hours’
然后将文档按句子切分，找出‘x hours’所在的句子
要求句子含有duties等PATTERN中的字眼，筛选出的句子中再找是maximum还是minimum的工作时长
然后以工作时长开头，查找工作周期，eg:'20 hours per week'中的week
'''
PATH = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\BUG'
# PATH = u'I:\\consulting agreement'

PATTERN = re.compile('consulting services|duties|engagement|services|consulting period|consulting',re.I|re.M)
MAX = re.compile('more than|maximum|up to|exceed|in excess of',re.I|re.M)
MIN = re.compile('less than|minimum|at least|no less',re.I|re.M)
WORKLOAD = re.compile('[\(\)\d\,]+\s+hours',re.M)
TIME_PATTERN = re.compile('week|year|month|day|quarter',re.I)

def find_workload(file):
    # find all work hours
    workload_list = WORKLOAD.findall(file)
    # 取一整句
    sentence = file.split('. ')
    # begin searching

    for hour in workload_list:
        for i in range(len(sentence)):
            if hour in sentence[i]:
                max=0;min=0;nm=0
                # sentence[i] = sentence[i].replace('-','')
                if PATTERN.search(sentence[i]):
                    if MAX.search(sentence[i]):max = hour.strip('hours').replace('(','').replace(')','')
                    elif MIN.search(sentence[i]):min = hour.strip('hours').replace('(','').replace(')','')
                    else: nm = hour.strip('hours').replace('(','').replace(')','')
                    # 以时间开头，在一小段字符内寻找工作周期
                    hour = hour.replace('(','\(').replace(')','\)')
                    CUT = hour +'[\s\w\d\,\:\(\)\"\-\\\/]{0,30}'
                    CUT = re.compile(CUT,re.M)
                    cut = CUT.search(sentence[i])
                    if cut:
                        cut=cut.group()
                        match = TIME_PATTERN.search(cut)
                        if match:
                            period = match.group()
                            return min,max,nm,period
                        else:
                            period=''
                            return min,max,nm,period
                    # try:
                    #     CUT = hour +'[\s\w\d\,\:\(\)\"\-\\\/]{0,30}'
                    #     CUT = re.compile(CUT,re.M)
                    #     cut = CUT.search(sentence[i]).group()
                    #     match = TIME_PATTERN.search(cut)
                    #     if match:
                    #         period = match.group()
                    #         return min,max,nm,period
                    # except StandardError:
                    #     period=''
                    #     return min,max,nm,period
                        # f_error = open('re_not_fit.txt', 'a')
                        # f_error.write(filename+'\n')
                        # f_error.close()
                        # break

def export_info(info1, info2, info3,info4):
    f_out = open('get_workload.txt', 'a')
    f_out.write(info1+'\t'+info2+'\t'+info3+'\t'+info4+'\n')
    f_out.close()

def main():
    count = 1
    for rt,dirs,files in os.walk(PATH):
        for file in files:
            root = os.path.join(rt,file)
            file_open = open(root)
            current_file = file_open.read()
            file_open.close()
            current_file = ' '.join([line.strip() for line in current_file.split('\n')])
            print 'Dealing with %dth file...' %count
            # print 'file:',file
            answer = find_workload(current_file)
            if answer:
                min = answer[0]
                max = answer[1]
                nm = answer[2]
                period = answer[3]
                if min==0:min=' '
                if max==0:max=' '
                if nm==0:nm=' '
                tmp = nm+' '+period
                export_info(file.rstrip('.txt'),max,min,tmp)
            else:
                export_info(file.rstrip('.txt'), ' ',' ',' ')
            count += 1

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start
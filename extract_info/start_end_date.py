#!/usr/bin/python2.7 -tt
# -*- coding: UTF-8 -*-
import os, re, time
'''
代码使用介绍：
python版本为2.7.11，采用的编译器为Anconda2
算法介绍：
1. 分别利用START和END的pattern找开始日期date1和结束日期date2；
2. 找start与end的pattern找日期；
3. 如果date1或者date2有超过一个，回溯到日期所在段落，确定段落名为term及相关pattern
4. 如果找不到符合的日期，则返回contracting date（第一个日期)作为star date
***
没有明显日期的尚未进行处理
'''
# PATH = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\BUG'
PATH = u'I:\\consulting agreement'

# 日期的全局变量,日期有如下格式：June 9,1995\28-Apr-96\1st day of June,1999
PATTERN1 = '((january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|\
jun|jul|aug|sep|sept|oct|nov|dec)[/\-\,\s\_]+\d+[/\-\,\s\_]+\d{2,4})'
PATTERN2 = '|(\d{1,2}[/\-\,\s\_]+(january|february|march|april|may|june|july|august|september|october|november|\
december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[/\-\,\s\_]+\d{2,4})'
PATTERN3 = '|([0-9]+[st|th|rd|nd][/\-\,\s\_\w]+(january|february|march|april|may|june|july|august|september|october|\
november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[/\-\,\s\_]+\d{2,4})'
PATTERNS = '('+PATTERN1 + PATTERN2 + PATTERN3+')'
date_pattern = re.compile(PATTERNS, re.I | re.M)

# 开始日期前的词组、结束日期的词组、开始与结束日期的词组模板
tmp_start = '(commence\s+on|commencing\s+on|commencing|effective\s+as\s+of|termination of employment is after\
|commence\s+as\s+of|commencing\s+as\s+of)\s+'
tmp_end = '(ending\s+on|terminate\s+on|expire\s+on|ending|end\s+before|terminating|continue\s+until)\s+'
start_end = '(from\s+)'+PATTERN1+'( through)( and)( including )'+PATTERN1+'|(between )'+PATTERN1+'(\s+and\s+)'+PATTERN1
START_END = re.compile(start_end,re.M|re.I)

# term相关标题
TERM = re.compile('term|termination|commencement',re.I)
# 文档输出
def export_info(info1, info2,info3):
    f_out = open('start_end_date.txt', 'a')
    f_out.write(info1+'\t'+info2+'\t'+info3+'\n')
    f_out.close()

# 找出目标词所在的段落开头标题,并判断标题里是否有term相关词，有的话作为所求时间返回
def passage(word_list,file):
    sentence = re.split('\;|\. ',file)
    # print 'word_list:',word_list
    for word in word_list:
        for i in range(len(sentence)):
            if word in sentence[i]:
                # 判断前一句是否为段落标题
                # print 'sentence[i]:',sentence[i]
                try:
                    if len(sentence[i-1])<32 and TERM.match(sentence[i-1]):
                        return word
                    elif len(sentence[i-2])<32 and TERM.match(sentence[i-2]):
                        # print 'i-1'
                        return word
                    elif len(sentence[i-3])<32 and TERM.match(sentence[i-3]):
                        # print 'i-2'
                        return word
                    elif i == 0 or i == 1:return word
                except:pass
    # 明明有许多时间符合关键字，但却没有一个的标题为term相关，返回第一个。由于情况过多，只能这样。
    return word_list[0]

def has_digit(a):
    if str(0) in a:return True
    if str(1) in a:return True
    if str(2) in a:return True
    if str(3) in a:return True
    if str(4) in a:return True
    if str(5) in a:return True
    if str(6) in a:return True
    if str(7) in a:return True
    if str(8) in a:return True
    if str(9) in a:return True

# 算法部分
def start_end_date(file):
    start_list = [];end_list = [];eff_date = []
    file = ' '.join([line.strip() for line in file.split('\n')])
    date_list = date_pattern.findall(file)
    if len(date_list) == 0: return None,None
    # 如果list中只有一个，则输出
    if len(date_list) == 1:
        # print 'only one:', date_list[0][0]
        return date_list[0][0],None
    for i in date_list:
        # print 'date:',i[0]
        # 搜索开始日期的词组，如commence on October 1, 1999、January 1, 1999 (the "Effective Date")
        start1 = tmp_start +'('+i[0]+')'
        START = re.compile(start1, re.M)
        cut = '[\s\w\d\,\:\(\)\"\-\.]{0,30}'+ i[0] +'[\s\w\d\,\:\(\)\"\-\.]{0,30}'
        CUT = re.findall(cut,file)
        for chunk in CUT:
            if 'Effective Date' in chunk and 'ending' not in chunk:
                start_list.append(i[0])
                eff_date.append(i[0])
        # 搜索结束日期的词组，如terminate on September 30, 2000
        end1 = tmp_end  +'('+i[0]+')'
        END = re.compile(end1,re.M)
        match_start = START.search(file)
        match_end = END.search(file)
        # 开始匹配
        if match_start:
            start_list.append(i[0])
        elif match_end:
            end_list.append(i[0])

    # 搜索开始日期与结束日期的词组，如from January 1, 1998 through and including December 31, 1998
    ls = START_END.findall(file)
    for i in ls:
        ls1 = []
        for j in range(len(i)):
            try:
                if len(i[j]) > 9 and has_digit(i[j]):
                    # 将搜索出来的词组中的日期（长度超过9并且含有数字）转为列表格式
                    ls1.append(i[j])
            except:continue
        # 去掉列表中重复的日期
        ls2 = []
        for k in ls1:
            if k not in ls2:ls2.append(k)
        start_list.append(ls2[0]);end_list.append(ls2[1])

    if len(start_list) == 0: start_list.append(date_list[0][0])

    # print 'start_list:',start_list
    # print 'end_list:',end_list
    # 已经匹配完所有可能日期，去掉列表中重复的日期
    new_start = []; new_end = []
    for l in start_list:
        if l not in new_start:new_start.append(l)
    for m in end_list:
        if m not in new_end:new_end.append(m)

    # 如果list中超过一个，则回溯查看所在段落
    # print 'new_start:',new_start
    # print 'new_end:',new_end
    if len(new_start) == 1:
        start = new_start[0]
    else:
        start = passage(new_start,file)
    # elif len(eff_date) >=1:
    #     # print 'eff_date:',eff_date
    #     start = eff_date[0]
    if len(new_end) == 0:
        end = None
    elif len(new_end)==1:
        end = new_end[0]
    else:
        end = passage(new_end,file)
    # print 'start:',start
    # print 'end:',end
    return start, end


def main():
    count = 1
    for rt,dirs,files in os.walk(PATH):
        for file in files:
            root = os.path.join(rt,file)
            file_open = open(root)
            current_file = file_open.read()
            file_open.close()
            print 'Dealing with %dth file...' %count
            print 'file:',file
            anwer = start_end_date(current_file)
            start = anwer[0]; end = anwer[1]
            if start and end:
                export_info(file.rstrip('.txt'), start, end)
            elif start:
                export_info(file.rstrip('.txt'), start, ' ')
            elif end:
                export_info(file.rstrip('.txt'), ' ', end)
            else:
                export_info(file.rstrip('.txt'), ' ', ' ')
            count += 1

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start
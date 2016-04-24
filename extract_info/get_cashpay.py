#!/usr/bin/python2.7 -tt
# -*- coding: UTF-8 -*-
import re,os,time
'''
代码使用介绍：
python版本为2.7.11，采用的编译器为Anconda2
算法介绍：
直接读取文档，搜索所有带$的金钱，截取$所在句子，如果符合PATTERN而没有NOISE（*经观察share和stock
部分也经常会在compensation的章节里，但不是所求。
找到合适的$后，以$为中心左右以20个字符的速度搜索段落TIME，默认距离$最近的时间为cashpay的频率
只要找到一个符合条件的cashpay就退出搜索
'''
# PATH = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\BUG'
PATH = u'I:\\consulting agreement'

PATTERN = re.compile('compensation|consideration|remuneration|services|consulting period|consulting fees',re.I|re.M)
NOISE = re.compile('insurance|tax|taxes|profit',re.I|re.M)
CASH = re.compile('\$[\,\.\d]+')
TIME_PATTERN = re.compile('hour|hours|year|yearly|annual|annum|month|monthly|day|daily|quarter',re.I)

def cash_not_with_share(money,passage):
    DANGER = re.findall('[\w\d\$\s\.\,]{13}share[\w\d\$\s\.\,]{13}',passage)
    for i in range(len(DANGER)):
        if money in DANGER[i].split(' '):
            return False
    else:
        return True

def find_cashpay(filename,file):
    store_dict = {}
    # find all $
    cash_list = CASH.findall(file)
    # print 'cash_list:', cash_list
    file = file.split('. ')
    '''
    get passages that includes cash, and store them in the form of dictionary
    for future verification
    '''
    # for cash in cash_list:
    #     for i in range(len(file)):
    #         if cash in file[i]:
    #             if not NOISE.search(file[i]) and PATTERN.search(file[i]):
    #                 CASH_PASSAGE = file[i]
    #             else:
    #                 try:
    #                     if len(file[i-1])>10 and len(file[i+1])>10:
    #                         CASH_PASSAGE = file[i-1]+file[i]+file[i+1]
    #                     elif len(file[i-1])<10 or len(file[i+1])<10:
    #                         CASH_PASSAGE = file[i-2]+file[i-1]+file[i]+file[i+1]+file[i+2]
    #                     elif len(file[i+2])<10 or len(file[i+2])<10:
    #                         CASH_PASSAGE = file[i-3]+file[i-2]+file[i-1]+file[i]+file[i+1]+file[i+2]+file[i+3]
    #                     else:
    #                         CASH_PASSAGE = file[i-4]+file[i-3]+file[i-2]+file[i-1]+file[i]+file[i+1]+file[i+2]+file[i+3]+file[i+4]
    #                 except IndexError:
    #                     index_error = open('index_error.txt','a')
    #                     index_error.write(filename+'\t'+cash+'\n')
    #                     index_error.close()
    #                     continue
    #             store_dict[cash] = CASH_PASSAGE
    '''begin searching'''
    for cash in cash_list:
        for i in range(len(file)):
            if cash in file[i]:
                # print 'cash:',cash
                # in case dots are used in names
                if not NOISE.search(file[i]) and PATTERN.search(file[i]):
                    CASH_PASSAGE = file[i]
                else:
                    try:
                        if len(file[i-1])>10 and len(file[i+1])>10:
                            CASH_PASSAGE = file[i-1]+file[i]+file[i+1]
                        elif len(file[i-1])<10 or len(file[i+1])<10:
                            CASH_PASSAGE = file[i-2]+file[i-1]+file[i]+file[i+1]+file[i+2]
                        elif len(file[i+2])<10 or len(file[i+2])<10:
                            CASH_PASSAGE = file[i-3]+file[i-2]+file[i-1]+file[i]+file[i+1]+file[i+2]+file[i+3]
                        else:
                            CASH_PASSAGE = file[i-4]+file[i-3]+file[i-2]+file[i-1]+file[i]+file[i+1]+file[i+2]+file[i+3]+file[i+4]
                    except IndexError:
                        # index_error = open('index_error.txt','a')
                        # index_error.write(filename+'\t'+cash+'\n')
                        # index_error.close()
                        continue

                if not NOISE.search(CASH_PASSAGE) and PATTERN.search(CASH_PASSAGE)and cash_not_with_share(cash,CASH_PASSAGE):
                    qualified_passage = CASH_PASSAGE
                    # expand search range till catch TIME_PATTERN
                    # print 'qualified_passage:',qualified_passage
                    if 'sum of '+cash in qualified_passage:
                        # print 'the sum of '
                        return cash, 'sum'
                    for i in range(0,len(qualified_passage)/2,20):
                        # CUT = '[\s\w\d\,\:\(\)\"\-\.]{0,'+ str(i) +'}?\\'+ cash +'[\s\w\d\,\:\(\)\"\-\.]{0,' + str(i) +'}?'
                        CUT = '[\s\w\d\,\:\(\)\"\-\.]{0,'+ str(i) +'}?\\'+ cash +'[\s\w\d\,\:\(\)\"\-\.]{' + str(i) +'}?'
                        # print CUT
                        try:
                            SEARCH = re.search(CUT, qualified_passage).group()
                            match = TIME_PATTERN.search(SEARCH)
                            if match:
                                paytime = match.group()
                                # print 'ooook',cash,paytime
                                return cash, paytime
                                # return cash, paytime,str(store_dict).lstrip('{').rstrip('}')
                        except StandardError:
                            # print 'cannot expand:',qualified_passage
                            # f_error = open('re_not_fit.txt', 'a')
                            # f_error.write(filename+'\n')
                            # f_error.close()
                            break
    else:
        return 'no match'

def export_info(info1, info2, info3):
    f_out = open('get_cashpay3.txt', 'a')
    f_out.write(info1+'\t'+info2+'\t'+info3+'\n')
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
            print 'file:',file
            answer = find_cashpay(file,current_file)
            if answer != 'no match':
                cash = answer[0]
                paytime = answer[1]
                # store = answer[2]
                # export_info(file.rstrip('.txt'), cash, paytime, store)
                export_info(file.rstrip('.txt'), cash, paytime)
                # print file
                # print cash
                # print paytime
            else:
                export_info(file.rstrip('.txt'), ' ',' ')
            count += 1

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start
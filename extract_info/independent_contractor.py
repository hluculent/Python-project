#!/usr/bin/python2.7 -tt
# -*- coding: UTF-8 -*-
import re, os, time
'''
代码使用介绍：
python版本为2.7.11，采用的编译器为Anconda2
算法介绍：
在文中找到independent contractor则返回1，找到与current employee相关的词则返回0
对于两种情况皆非的文档，将文档名及前五句话（一段左右。因为文档不以换行符换行，所以以句子分割）
另存为independent_contractor_note.csv
'''
# PATH = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\BUG'
PATH = u'I:\\consulting agreement'

PATTERN = re.compile('independent\s+contractor.|independent consulting',re.I|re.M)
NOISE = re.compile('has served the company|continue as a director|has been employed by the|\
is employed by the company|continue as a consultant|provide for the continuing services|\
the future consulting services|maintain a relationship with|\
desire to retain [\'\s\w]{5,20} services as a Consultant|has been employed by|\
will remain an employee|current employee', re.M)


def independent_contractor(filename,file):
    if PATTERN.search(file): return str(1)
    else:
        file1 = file[:int(len(file)/5)]
        file1 = ' '.join([line.strip() for line in file1.split('\n')])
        if NOISE.search(file1): return str(0)
        else:
            file = ' '.join([line.strip() for line in file.split('\n')])
            sentence = file.split('. ')
            try:
                note = sentence[0]+'. '+sentence[1]+'. '+sentence[2]+'. '+sentence[3]+'. '+sentence[4]+'. '
                f = open('independent_contractor_note.txt', 'a')
                f.write(filename+'\t'+note+'\n')
                f.close()
            except:
                f = open('independent_contractor_note.txt', 'a')
                f.write(filename+'\t'+str(sentence)+'\n')
                f.close()

def export_info(info1, info2):
    f_out = open('independent_contractor.txt', 'a')
    f_out.write(info1+'\t'+info2+'\n')
    f_out.close()

def main():
    count = 1
    ic_count=0;ce_count=0
    for rt,dirs,files in os.walk(PATH):
        for file in files:
            root = os.path.join(rt,file)
            file_open = open(root)
            current_file = file_open.read()
            file_open.close()
            print 'Dealing with %dth file...' % count
            # print 'file:',file
            answer = independent_contractor(file, current_file)
            if answer == '1':
                ic_count += 1
                export_info(file.rstrip('.txt'), answer)
            elif answer == '0':
                ce_count += 1
                # print file
                export_info(file.rstrip('.txt'), answer)
            else:
                export_info(file.rstrip('.txt'), ' ')
            count += 1
        print ic_count,ce_count

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start

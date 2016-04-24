#!/usr/bin/python2.7 -tt
# -*- coding: UTF-8 -*-
import re,os

PATH = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\BUG'

CONSUL_PAT = re.compile('consultant|Executive', re.I)
# <_sre.SRE_Pattern object at 0x0000000002C5F4E0> <type '_sre.SRE_Pattern'>
COMPANY_PAT = re.compile('company', re.I)
def find_consultant_zipcode(file):
    # a = re.compile(' *')
    # file = re.sub(a, '_', file)
    # file = file_with_space.replace('', '_')
    # file2 = file1.replace('          ','-')
    # file = file2.replace('     ', '>')
    pattern = re.compile('[0-9]{5}')
    length = int(len(file)/4)
    match_front = pattern.findall(file, 0, length)
    print 'match_front:', match_front
    match_back = pattern.findall(file, length)
    print 'match_back:', match_back
    matches = match_front + match_back
    # print matches
    if matches:
        for i in range(len(matches)):
            print 'matches[i]:', matches[i]
            chunk = '(.{30,130}?)(' + matches[i] + ')(.{0,30})'
            # request: 如果邮编后面没有字符，chunk后面加上(.{30}?)时无法得出结果
            pattern = re.compile(chunk,re.S)
            match_front = pattern.findall(file, 0, length)
            print 'match_front', match_front
            match_back = pattern.findall(file, length)
            print 'match_back', match_back
            match = match_front + match_back
            print 'find in:',match
            for j in range(len(match)):
                match_str = ''
                for k in match[j]:
                    match_str += k
                    print 'match[j]:', match[j]
                print 'match_str:', match_str
                    # print 'k:', k
                    # search = k.split(' ')
                    # print 'search:', search
                found_keyword = CONSUL_PAT.search(match_str)
                found_noise = COMPANY_PAT.findall(match_str)
                print 'found_noise',found_noise
                if not found_noise and found_keyword :
                    print 'FOUND:',match[j][1]
                    return match[j][1]
                    # if ('Consultant:' in search) or ('CONSULTANT' in search):
                    #     print match[j][1]
                    #     return match[j][1]
        else:
            return 'STANDARD FAIL'
    else:
        return 'NO 5 DIGIT FOUND'

for rt,dirs,files in os.walk(PATH):
    for file in files:
        root = os.path.join(rt,file)
        file_open = open(root)
        current_file = file_open.read()
        file_open.close()
        # text=[]
        # for line in current_file.split('\n'):
        #     if line.strip() != '\n':
        #         line = line.strip()
        #         text.append(line)
        #         text.append('\n')
        # text_all = ' '.join(text)
        # print 'text:',text_all
        current_file = ' '.join([line.strip() for line in current_file.split('\n')])
        # print current_file
        print 'file:',file
        str(find_consultant_zipcode(current_file))


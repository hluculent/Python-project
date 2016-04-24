#!/usr/bin/python2.7 -tt
# -*- coding: UTF-8 -*-
import os, re, time
# import nltk

"""
代码使用介绍：
python型号为2.7.11，采用的编译器为Anconda2
在搜索人名的时候使用了nltk包，其编译后的文件已经包含。修改路径名后代码应该能正常运行。
运行时会显示正在处理第几个文档，结束后有总时长。运行结果包含在result.txt中，可以直接导入excel/csv。
10个sample文档处理时间为23秒，正确率未检验。
"""
"""
算法介绍：
为了和前面抽取资料的文件顺序保持一致，首先将exfilename那列导出txt,路径path0
put_tag函数做的就是在给文件名前面写一个和csv同样顺序的数字标签，方便以后校对
get_filename函数和find函数：对应ptah0的顺序读出文档名，在path中打开对应文档
find_contracting_date函数实现查找合约日期，默认文档开头第一个提到的日期为目标，包含多种格式（目前一种）
find_consultant_name将文档中含有的名字全部提出后，一个个搜索其附近是否出现consultant/consel字眼，若提到则输出，否则输出提到的第二个
（根据文本和代码运行结果观察，第一个为公司名。*不一定正确）
find_governing_law函数先抽取出州名，同样搜索附近是否出现governing law/governed，否则搜索state，若无结果者输出提到次数最多的
find_consultant_zipcode函数在文档前1/4与后1/4找出5位数，与前面查到的地名/人名进行交叉确认
find_confidentiality与find_non_compete都是查询关键字，若无则默认未提及，返回0
最后按照number, exfilename, contracting_date, consultant, zipcode, law, confidentiality, non_compete顺序输出结果
"""
# 需要处理的文件夹
path = u'I:\\consulting agreement'
# 存放文档对应csv顺序的txt路径
path0 = u'E:\\最近任务\\实习资料\\姚老师\\2.7_consulting_agreement_info\\read_sequence.txt'

# 日期的全局变量,日期有如下格式：June 9,1995\28-Apr-96\1st day of June,1999
PATTERN1 = '((january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)([/\-\,\s\_]+)(\d+)([/\-\,\s\_]+)(\d){2,4})'
PATTERN2 = '|((\d){1,2}([/\-\,\s\_]+)(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)([/\-\,\s\_]+)(\d){2,4})'
PATTERN3 = '|([0-9]+[st|th|rd|nd]([/\-\,\s\_\w]+)(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)([/\-\,\s\_]+)(\d){2,4})'
PATTERNS = PATTERN1 + PATTERN2 + PATTERN3
date_pattern = re.compile(PATTERNS, re.I | re.M)

# 州名的全局变量
states = re.compile('\s(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut\
|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky\
|Louisiana|Maine|Massachusetts|Maryland|Michigan|Minnesota|Mississippi\
|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico\
|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania\
|Rhode|South Cardinal|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia\
|Washington|West Virginia|Wisconsin|Wyoming)', re.I|re.M)

# zipcode交叉检查的全局变量
CONSUL_PAT = re.compile('consultant|Executive', re.I)
COMPANY_PAT = re.compile('company', re.I)

# 将csv的exfilename复制到txt后，在txt上为文档名前面加上csv的列序号
def put_tag():
    f1 = open(path0)
    fn = f1.readlines()
    for i in range(0,len(fn)):
        fn[i] = str(i+1) + '\t' + fn[i]
    f1.close()
    f2 = open(path0, 'w')
    f2.writelines(fn)
    f2.close()

# 得到txt里的文档名和序号，以字典形式输出
def get_filenames_dict(path):
    fns = open(path).readlines()
    filenames_dict = {}
    for i in range(1, len(fns)):
        fn = fns[i]
        number = fn.split('\t')[0]
        exfilename = fn.split('\t')[1].replace('\n', '')+'.txt'
        filenames_dict[exfilename] = number
    return filenames_dict

# 输出碰到的第一个日期（即最靠近合同标题）
def find_contracting_date(file):
    match = date_pattern.search(file)
    if match:
        return match.group()

# 在文档前1/4寻找consultant而不搜索完全部文档，可加速
def find_consultant_name(file):
    file_front = file[0:int(len(file)/4)]
    tokens = nltk.tokenize.word_tokenize(file_front)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    for i in range(len(person_list)):
        chunk = '([\s\w\,\(\)\.]{50}?)(' + person_list[i] + ')([\s\w\,\(\)\.]{50}?)'
        pattern = re.compile(chunk, re.M)
        match = pattern.findall(file)
        for j in range(len(match)):
            for k in match[j]:
                search = k.split(' ')
                if ('consultant' in search) or ('consel' in search):
                    return match[j][1]
    else:
        if len(person_list) > 2:
            return person_list[1]
        else:
            return 'Not Found'
    """
    通过调查文档发现，有时别的名字会比目标先通过‘在consultant’这个词附近而直接返回结果。
    下一步的工作是把符合条件的弄成list，再计算频率，靠近consultant的次数越多，则更可能为目标
    """

# 先抽取出州名，同样搜索附近是否出现governing law/governed，否则搜索state，若无结果者输出提到次数最多的 *由于观察的文档不多，这种规则不一定对
def find_governing_law(file):
    matches = states.findall(file)
    if matches:
        for i in range(len(matches)):
            chunk = '([\s\w\,\(\)\.]{30}?)(' + matches[i] + ')([\s\w\,\(\)\.]{30}?)'
            pattern = re.compile(chunk,re.M)
            match = pattern.findall(file)
            # 开始进行筛选
            for j in range(len(match)):
                for k in match[j]:
                    search = k.split(' ')
                    # if ('[Ll][Aa][Ww][Ss]' in search) or ('governed' in search):
                    if ('laws' in search) or ('governed' in search):
                        return match[j][1]
                    elif 'State' in search:
                        return match[j][1]
            #else:
                #return matches[0]
    else:
        return None

# 在文档前1/4和后1/4寻找邮编，找到后再次查找邮编附近是否有consultant的名字或者所在地名(law)
def find_consultant_zipcode(file0):
    file = ' '.join([line.strip() for line in file0.split('\n')])
    pattern = re.compile('[0-9]{5}')
    length = int(len(file)/4)
    match_front = pattern.findall(file, 0, length)
    match_back = pattern.findall(file, length)
    matches = match_front + match_back
    if matches:
        for i in range(len(matches)):
            chunk = '(.{30,130}?)(' + matches[i] + ')(.{0,30}?)'
            pattern = re.compile(chunk,re.S)
            match_front = pattern.findall(file, 0, length)
            match_back = pattern.findall(file, length)
            match = match_front + match_back
            for j in range(len(match)):
                match_str = ''
                for k in match[j]:
                    match_str += k
                # 过滤： 在邮编附近出现consultant而不出现company
                found_keyword = CONSUL_PAT.search(match_str)
                found_noise = COMPANY_PAT.findall(match_str)
                if not found_noise and found_keyword:
                    return match[j][1]
        else:
            return 'NoMatch'
    else:
        return None
# error1是连五位数都找不到
# error2是按照搜索要求过滤后没有符合要求的五位数

def find_confidentiality(file):
    # 有confidential、confindentiality、disclosed、disclosure等情况
    # 更有提到non-confidential，但是是反用的情况
    # 因此默认提到相关字眼的，一定是要遵循协议的
    pattern1 = re.compile('confidential',re.I|re.M)
    pattern2 = re.compile('disclosure',re.I|re.M)
    pattern3 = re.compile('disclosed',re.I|re.M)
    match1 = pattern1.search(file)
    match2 = pattern2.search(file)
    match3 = pattern3.search(file)
    if match1 or match2 or match3:
        return 1
    else:
        return 0

def find_non_compete(file):
    # 出现同意不参与competition的情况，但比较少
    # 除了目标词外，经常有competitor、competitive、competing、competence等干扰词
    # 所以还是以noncompetition为主
    pattern = re.compile('non[-\s]?compet', re.I | re.M)
    match = pattern.search(file)
    if match:
        return 1
    else:
        return 0

def export_info(info1, info2, info3, info4, info5, info6,info7):
    f_out = open('5info.txt', 'a')
    f_out.write(info1+'\t'+info2+'\t'+info3+'\t'+info4+'\t'+info5+'\t'+info6+'\t'+ info7+'\n')
    f_out.close()

def main():
    # put_tag()
    count = 1
    names = get_filenames_dict(path0)
    for rt,dirs,files in os.walk(path):
        for file in files:
            number = names.get(file)
            if file not in names:
                f_error = open('not_in_dir.txt', 'a')
                f_error.write(str(number)+'\t'+str(file))
                f_error.close()
            else:
                root = os.path.join(rt,file)
                file_open = open(root)
                current_file = file_open.read()
                file_open.close()
                print 'Dealing with %dth file...' %count
                contracting_date = str(find_contracting_date(current_file)).replace('\n', '')
                confidentiality = str(find_confidentiality(current_file))
                non_compete = str(find_non_compete(current_file))
                # consultant = str(find_consultant_name(current_file)).replace('\n', '')
                law = str(find_governing_law(current_file))
                zipcode = str(find_consultant_zipcode(current_file))
                export_info(number, file.rstrip('.txt'), contracting_date, zipcode, law, confidentiality, non_compete)
                count += 1

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start

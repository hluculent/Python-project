#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import time
import PyPDF2

# this path should be changed accordingly
path = u'E:\\最近任务\\实习资料\\姚老师\\2.7_R_to_Python\\Ver3\\crashrisk'
# count crash risk
pattern = re.compile(r'crash\s?risk', re.I | re.M)

def words_count(text):
    #count = len(re.findall('[Cc]rash [Rr]isk', text))+ len(re.findall('[Cc]rash[Rr]isk', text))
    count = len(pattern.findall(text))
    return count

# create a new text to store pdfname and words_count, then convert it to excel
def write_into_txt(pdfname, count):
    database = open(r'database17.txt', 'a')
    database.write(pdfname + '\t' + str(count) + '\n')
    # contents are saved in this format in .txt, later can be imported into an excel directly
    database.close()


def main():
    pdf_num = 0
    for rt, dirs, files in os.walk(path):
        for f in files:
            #start = time.clock()
            #just look for pdf files
            if not f.endswith('.pdf'):
                continue
            else:
                pdf_num += 1
                print 'Dealing with the %dth pdf...' % pdf_num
                root = os.path.join(rt,f)
                #extract pdf using pypdf2
                try:
                    pdf_file = open(root, "rb")
                    pdf_obj = PyPDF2.PdfFileReader(pdf_file)
                    text = ''
                    for page in pdf_obj.pages:
                        text += page.extractText()
                    count = words_count(text)
                    pdf_file.close()
                except ValueError:
                    f1 = open('cannot_read.txt','w')
                    f1.write(str(f))
                    f1.close()
                #end = time.clock()
                #print end - start
                #if count=0 remove this file from the directory
                if count == 0:
                    try:
                        os.remove(root)
                    except:
                        f2 = open('cannot_remove.txt','w')
                        f2.write(str(f))
                        f2.close()
                write_into_txt(f, count)

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start

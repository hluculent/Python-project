#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import re
import time
import PyPDF2

#this path should be changed accordingly
path = u'E:\\最近任务\\实习资料\\姚老师\\BoardEx'

#count M&A and [Mm]ergers and [Aa]cquisitions
def words_count(text, root):
    count = len(re.findall('[Mm]ergers and [Aa]cquisitions', text)) + \
            len(re.findall(r'M&A', text))

    return count

#create a new text to store pdfname and words_count, then convert it to excel
def write_into_txt(pdfname, count):
    database = open('database.txt', 'a')
    database.write(pdfname + '\t' + str(count) + '\n')
    #contents are saved in this format in .txt, later can be imported into an excel directly
    database.close()


def main():
    pdf_num = 0
    for rt, dirs, files in os.walk(path):
        for f in files:
            #just look for pdf files
            if not f.endswith('.pdf'):
                continue
            else:
                pdf_num += 1
                print 'Dealing with the %d pdf...' % pdf_num
                pdfname = os.path.join(f)
                root = os.path.join(rt,f)
                pdf_file = open(root, "rb")
                #extract pdf using pypdf2
                pdf_obj = PyPDF2.PdfFileReader(pdf_file)
                text = ''
                for page in pdf_obj.pages:
                    text += page.extractText()
                count = words_count(text, root)
                #if count=0 remove this file from the directory
                if count == 0:
                    pdf_file.close()
                    os.remove(root)
                write_into_txt(pdfname, count)

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start

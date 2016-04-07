#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
To count how many times 'M&A' or '[Mm]ergers and [Aa]cquisitions' occures in each pdf.
According to random sampling, it acheives an accuracy of about 90%.
Path should be changed accordingly before run.
"""
import os
import re
import time
#from pdfminer import pdf2text
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

# this path should be changed accordingly
path = u'E:\\最近任务\\实习资料\\姚老师\\2.7_R_to_Python\\70_crashrisk_pdf'
# 存放文档对应csv顺序的txt路径
path0 = u'E:\\最近任务\\实习资料\\姚老师\\2.7_R_to_Python\\70_crash_risk.txt'
# count crash risk
pattern = re.compile(r'crash\s?risk', re.I | re.M)

def get_filenames(path):
    filename = []
    fns = open(path).readlines()
    for i in range(len(fns)):
        fn = fns[i].replace('\n','')
        filename.append(fn)
    return filename

def convert_pdf_to_txt(path):
    outtype='txt'
    outfile = path[:-3] + outtype
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()
    if outfile:
        outfp = file(outfile, 'w+')
    else:
        outfp = sys.stdout
    device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    outfp.seek(0)
    text = outfp.read()
    outfp.close()
    return text

#count M&A and [Mm]ergers and [Aa]cquisitions
def words_count(text, root):
    count = 0
    count = len(pattern.findall(text))
    if count == 0:
        os.remove(root) 
    return count

#create a new text to store pdfname and words_count, then convert it to excel
def write_into_txt(pdfname, count):
    database = open('database_speed.txt', 'a')
    database.write(pdfname + '\t' + str(count) + '\n')
    #contents are saved in this format in .txt, later can be imported into an excel directly
    database.close()

#create a pdf path and read one by one, maybe there are more than one folder
def main():
    #this path should be changed accordingly
    pdf_num = 0
    names = get_filenames(path0)
    for rt, dirs, files in os.walk(path):
        for f in files:
            #just look for pdf files
            if not f.endswith('.pdf'):
                continue
            elif f not in names:
                continue
            else:
                pdf_num += 1
                print 'Dealing with the %dth pdf...' % pdf_num
                root = os.path.join(rt,f)
                text = convert_pdf_to_txt(root)
                count = words_count(text,root)
                write_into_txt(f, count)

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start


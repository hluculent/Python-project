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

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

#this path should be changed accordingly，全局变量
path = u'E:\\最近任务\\实习资料\\姚老师\\2.7_R_to_Python\\paper'
   
#convert pdf to text， extract code from PDFminer, see its GitHub homepage for details
def pdf_to_text(root):
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Extract text
    fp = file(root, 'rb')
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
    fp.close()
    # Get text from StringIO
    text = sio.getvalue()
    # Cleanup
    device.close()
    sio.close()

    return text

#count M&A and [Mm]ergers and [Aa]cquisitions
def words_count(text, root):
    count = 0
    count = len(re.findall('[Mm]ergers and [Aa]cquisitions', text)) + len(re.findall(r'M&A', text))
    if count == 0:
        os.remove(root) 
    return count

#if count=0 remove this file from the directory
    

#create a new text to store pdfname and words_count, then convert it to excel
def write_into_txt(pdfname, count):
    database = open('database2.txt', 'a')
    database.write(pdfname + '\t' + str(count) + '\n')
    #contents are saved in this format in .txt, later can be imported into an excel directly
    database.close()

#create a pdf path and read one by one, maybe there are more than one folder
def main():
    for rt, dirs, files in os.walk(path):
        for f in files:
            #just look for pdf files
            if not f.endswith('.pdf'):
                continue
            else:
                pdfname = os.path.join(f)
                root = os.path.join(rt,f)
                text = pdf_to_text(root)
                count = words_count(text,root)
                write_into_txt(pdfname, count)

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print end - start

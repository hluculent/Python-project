#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
To count how many times 'crash risk' occures in each pdf.
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

path = u'F:\\快盘\\sharebox\\jqyaoxjtu@gmail.com\\cuilan\\From Lu\\extraxt_pdf\\PDFMiner\\crashrisk'

pattern = re.compile(r'crash\s?risk', re.I | re.M)

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
    # print text
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
    database = open(r'count_pdfminer.txt', 'a')
    database.write(pdfname + '\t' + str(count) + '\n')
    #contents are saved in this format in .txt, later can be imported into an excel directly
    database.close()

#create a pdf path and read one by one, maybe there are more than one folder
def main():
    #this path should be changed accordingly
    pdf_num = 0
    for rt, dirs, files in os.walk(path):
        for f in files:
            #just look for pdf files
            if not f.endswith('.pdf'):
                continue
            else:
                pdf_num += 1
                print 'Dealing with the %dth pdf...' % pdf_num
                root = os.path.join(rt,f)
                text = pdf_to_text(root)
                count = words_count(text,root)
                write_into_txt(f, count)

if __name__ == '__main__':
    start = time.clock()
    main()
    end = time.clock()
    print 'Total time: ', end - start

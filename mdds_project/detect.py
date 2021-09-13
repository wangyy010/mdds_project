#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

"""
MDDS的入口文件
"""
import env
import os
import sys
import traceback
# from mdds.lib.fileType import *
# from mdds.lib.configMgr import config
# from mdds.lib.dbMgr import DBMgr
# from mdds.lib.logger import set_logger
# import mdds.detect_engines.pdf.detect as pdf_detect
# import mdds.detect_engines.docx.detect as docx_detect
# import mdds.detect_engines.doc.detect as doc_detect
from lib.fileType import *
#from lib.configMgr import config
#from lib.logger import set_logger
import detect_engines.pdf.detect as pdf_detect
import detect_engines.docx.detect as docx_detect
import detect_engines.doc.detect as doc_detect
   
# DBManager = DBMgr()
#logger = set_logger(env.FILE, config.log_path)

sum = 0
def check_file(filename, calbFunc):
    result = None
    global sum
    sum = sum + 1
    try:
        file_type, data = get_type(filename)
        print 'check file: %s' %(filename)
        if file_type == PDF:
            result = [filename, 'PDF', pdf_detect.detect(data, filename),pdf_detect.describe(data,filename)]
        elif file_type == DOCX:
            result = [filename, 'DOCX', docx_detect.detect(data, filename),docx_detect.describe(filename)]
        elif file_type == DOC:
            result = [filename, 'DOC', doc_detect.detect(data, filename), doc_detect.describe(filename)]
        #elif file_type == OLE:
            #result = [filename, 'OLE', doc_detect.detect(data, filename), doc_detect.describe(filename)]
        elif file_type == 'others':
            'do in the future'
      
        if result:
            calbFunc(result)
    except:
        raise
    return result
   
   
def check_dir(dir, calbFunc):
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename = os.path.join(root, file)
            check_file(filename, calbFunc)
        for sub_dir in dirs:
            check_dir(sub_dir, calbFunc)
  
'''
def myCalbFunc(result):
    """对检测结果进行处理的函数，可以是界面展示的回调函数，存储数据库的回调函数等
    本函数是将检测结果保存到了数据库中
    输入：
        result: [filename, fileType, BAD/GOOD]
    """
    result[1] = str(result[1])
    DBManager.save_record(result)
 '''


def main(source, calbFunc):
    """ 恶意文档检测系统入口
    输入：
        source: 一个文件夹或一个文档的绝对路径
        calbFunc: 一个处理检测结果的回调函数
    """
    if os.path.isdir(source):
        check_dir(source, calbFunc)
    elif os.path.isfile(source):
        check_file(source, calbFunc)
    else:
        print source
    # DBManager.force_save_records()
    
'''
if __name__ == '__main__':
    source = sys.argv[1]
    main(source, myCalbFunc)
'''
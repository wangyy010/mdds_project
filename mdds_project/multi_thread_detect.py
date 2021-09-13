#!usr/bin/env python 2.7
# -*- coding: utf-8 -*-

"""
MDDS多线程版本
"""

import env
import os
import sys
import traceback
from detect import check_file
#from mdds.lib.configMgr import config
import threading
import Queue
#from mdds.lib.logger import set_logger
# from mdds.lib.dbMgr import DBMgr
from lib.configMgr import config



# DBManager = DBMgr()
#logger = set_logger(env.FILE, config.log_path)
THREAD_NUM = int(config.thread_num)
DBLock = threading.Lock()


def check_thread(thread_queue, calbFunc):
    while(1):
        task = thread_queue.get()
        if task != None:
            check_file(task, calbFunc)
        else:
            thread_queue.put(None)
            break

   
class ThreadPool:
    """
    统一管理线程的类
    """
    def __init__(self, thread_num, calbFunc):
        self.thread_list = []
        self.queue = Queue.Queue()
        for i in xrange(thread_num):
            child_thread = threading.Thread(target = check_thread, args = (self.queue, calbFunc))
            self.thread_list.append(child_thread)
            
            
    def add_task(self, task):
        self.queue.put(task)
            
            
    def active(self):
        for child_thread in self.thread_list:
            child_thread.start()
            
            
    def wait(self):
        self.add_task(None)
        for child_thread in self.thread_list:
            child_thread.join()
   
 
def check_dir(dir, thread_pool):
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename = os.path.join(root, file)
            thread_pool.add_task(filename)
        for sub_dir in dirs:
            check_dir(sub_dir, thread_pool)
'''
def myCalbFunc(result):
    """对检测结果进行处理的函数，可以是界面展示的回调函数，存储数据库的回调函数等
        本函数是将检测结果保存到了数据库中
        输入：
            result: [filename, fileType, BAD/GOOD, describe]
    """
    DBLock.acquire()
    result[1] = str(result[1])
    DBManager.save_record(result)

    DBLock.release()
'''
def main(source, calbFunc):
    """ 恶意文档检测系统入口
    输入：
        source: 一个文件夹或一个文档的绝对路径
        calbFunc: 一个处理检测结果的回调函数
    """
    if os.path.isdir(source):
        thread_pool = ThreadPool(THREAD_NUM, calbFunc)
        thread_pool.active()
        check_dir(source, thread_pool)
        thread_pool.wait()
    elif os.path.isfile(source):
        check_file(source, calbFunc)
    else:
        print source
    #DBManager.force_save_records()


'''
if __name__ == '__main__':
    source = sys.argv[1]
    main(source, myCalbFunc)

'''
# -*- coding:utf-8 -*-
from __future__ import division
import os
import sys
import time
import sqlite3
import logging
import hashlib
from watchdog.observers import Observer
from watchdog.events import *
from module import *
from sqlalchemy.orm import sessionmaker
import time
import datetime
# import mdds.multi_thread_detect
import detect
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import ConfigParser
import os,platform
import codecs
import json
import collections
import base64
import chardet

# BUF_SIZE is totally arbitrary, change for your app!
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
OUTPUT_DIR="C:\\Users\\snRNA\\Documents\\mdds_linux\\testlog"  # log output directory
DB_DIR = "C:\\Users\\snRNA\\Documents\\mdds_linux\\test.db"  # Database file Directory
SUPERVIE_DIR = "C:\\Users\\snRNA\\Documents\\mdds_linux\\watchdogtest" # Directory needs to be supervised

cf = ConfigParser.ConfigParser()

if not os.path.exists("supervisor.conf"):
    print "Not find supervisor.conf in the same directory"
    exit(1)

cf.read("supervisor.conf")
OUTPUT_DIR = cf.get("supervisor", "OUTPUT_DIR")
SUPERVIE_DIR = cf.get("supervisor", "SUPERVIE_DIR")
CODE = cf.get("supervisor", "CODE")

def verifycode():
    global CODE
    codestring = ""
    try:
        codestring = base64.b64decode(CODE)
    except Exception:
        print "CODE error! exited!"
        sys.exit(1)
 #检查磁盘序列号（物理地址）
    codelist = codestring.replace("\n", "").replace("\r", "").split(":", 1)  #split("+", 1)
    allowtime = datetime.datetime.strptime(codelist[0], "%Y-%m-%d")
    nowtime = datetime.datetime.now()
    if nowtime > allowtime:
        print "Time expired! exited!"
        sys.exit(1)

    if platform.system().lower() == "windows":
        result = os.popen("wmic diskdrive get serialnumber")
        context = result.read()
        result.close()
        flag = 0
        for line in context.splitlines()[1:]:
            if line.strip() == codelist[1]:
                flag = 1
                break
        if not flag:
            print "Disk Serial Number wrong! exited"
            sys.exit(1)

    else:
        result = os.popen("cat /sys/class/net/*/address")
        context = result.read()
        result.close()
        flag = 0
        for line in context.splitlines()[:-1]:
            if line.strip() == codelist[1]:
                flag = 1
                break
        if not flag:
            print "Mac Address wrong! exited"
            sys.exit(1)



def getmd5sum(filepath):
    md5 = hashlib.md5()
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()


def getstrdecode(string):

    try:
        decode_str = string.decode("gb18030")
    except UnicodeDecodeError:
        decode_str = string.decode("utf-8")        

    return decode_str


def generatejson(result, md5):

    global OUTPUT_DIR
    filename = 'document' + time.strftime('%Y-%m-%d') + ".json"
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        fr = codecs.open(filepath, 'r', 'utf-8')
        read_list = fr.read()
        #print read_list
        if read_list == "":
            write_list = list()
        else:
            write_list = json.loads(read_list.encode('unicode-escape').decode('string_escape'))
        # fr.close()
        #write_list = json.loads(str(read_list).encode('utf-8'))
        #write_list = json.loads(read_list.encode('unicode-escape').decode('string_escape'))
        # print len(write_list)
        fr.close()
        write_dict = collections.OrderedDict()
        write_dict['fileName'] = getstrdecode(result[0])
        write_dict['MD5'] = md5
        write_dict['type'] = result[1]
        write_dict['result'] = 1 if result[2] else 0
        write_dict['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        write_list.append(write_dict)
        # print write_list
        # print len(write_list)
        fw = codecs.open(filepath, 'w', 'utf-8')
        fw.write(json.dumps(write_list, ensure_ascii=False))
        fw.close()
    else:
        write_dict = collections.OrderedDict()
        #print type(result[0])
        write_dict['fileName'] = getstrdecode(result[0])
        write_dict['MD5'] = md5
        write_dict['type'] = result[1]
        write_dict['result'] = 1 if result[2] else 0
        write_dict['created_at'] = time.strftime('%Y-%m-%d %H:%M:%S')
        write_list = list()
        write_list.append(write_dict)
        fw = codecs.open(filepath, 'a+', 'utf-8')
        fw.write(json.dumps(write_list, ensure_ascii=False))
        fw.close()


def calbFunc(result):
    #print (result)
    Session = sessionmaker(bind=engine)
    session = Session()
    md5sum = getmd5sum(result[0])
    # try:
    #     filename = result[0].decode('gbk')
    # except Exception:
    #     filename = result[0]
    #     print result[0]
    # print type(filename)
    ed_file = File(filename=getstrdecode(result[0]), hash=md5sum, type=result[1],
                   check_result=result[2],  created_at=time.strftime('%Y-%m-%d %H:%M:%S'),)
    session.add(ed_file)
    session.commit()
    session.close()
    generatejson(result, md5sum)


def generateLog():
    global  OUTPUT_DIR
    date = "16:44:00"
    Session = sessionmaker(bind=engine)
    session = Session()
    nowtime = datetime.datetime.now()
    # nowtime = time.strftime('%Y-%m-%d %H:%M:%S')
    beforetime = nowtime + datetime.timedelta(days=-1)
    files = session.query(File).filter(File.created_at.between(beforetime.strftime('%Y-%m-%d %H:%M:%S'), nowtime.strftime('%Y-%m-%d %H:%M:%S')))
    session.close()
    f = open(os.path.join(OUTPUT_DIR,"document_"+nowtime.strftime('%Y-%m-%d-%H-%M-%S')+".log"),'w+')
    for file in files:
        write_line = file.filename+","+file.hash+","+file.type+","+str(file.check_result)+","+file.created_at
        f.write(write_line.encode("utf-8"))
        f.write("\n")
    f.close()

    # for file in files:
    #     print(file.filename, file.type, file.created_at)



class MyHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_created(self, event):
        if not event.is_directory:
            # print ("The file is created",event.src_path)
            md5sum = getmd5sum(event.src_path)
            if md5sum is None:
                return
            # print(event.src_path," : ",md5sum)
            Session = sessionmaker(bind=engine)
            session = Session()
            a_flie = session.query(File).filter_by(hash=md5sum).first()
            session.close()
            if a_flie is None:
                detect.main(event.src_path, calbFunc)

            else:
                session.close()
                result = list()
                result.append(event.src_path)
                result.append(a_flie.type)
                result.append(a_flie.check_result)
                generatejson(result, a_flie.hash)

    def on_modified(self, event):
        if not event.is_directory:
            pass
            # print ("The file is updated", event.src_path)


if __name__ == "__main__":

    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # path = "C:\\Users\\snRNA\\Documents\\mdds_linux\\watchdogtest"
    # trigger = CronTrigger(day='*')
    # sched = BlockingScheduler()
    # sched.add_job(generateLog, 'cron', second='*/5')
    # sched.add_job(generateLog, trigger)
    verifycode()
    print "verify code success!"
    event_handler = MyHandler()
    print "Initially check is starting..."
    if os.listdir(SUPERVIE_DIR):
        detect.main(SUPERVIE_DIR, calbFunc)
    observer = Observer()
    observer.schedule(event_handler, SUPERVIE_DIR, recursive=True)
    print "Supervisor is starting...."
    observer.start()
    # sched.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

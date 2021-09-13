#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import numpy as np
import os
import ConfigParser
import sys
DIR = os.path.dirname
ABSPATH = os.path.abspath(__file__)
ROOT = DIR(ABSPATH)  # for  debug

DOC_CLASSIFIER = ROOT + r'\model\detect_model.txt' # for debug

cf = ConfigParser.ConfigParser()
path, filename = os.path.split(os.path.realpath(sys.argv[0]))
# cf.read(path + r'\config\config.ini')
cf.read(os.path.join(path,"config","config.ini"))
#ROOT = cf.get("enginespath", "doc")  # for generate
#DOC_CLASSIFIER = os.path.join(ROOT,"model","detect_model.txt")# for pyinstaller  #ROOT + r'\model\detect_model.txt'

BAD = True
GOOD = False

def get_doc_classifier():
    clf = None
    with open(DOC_CLASSIFIER, 'rb') as f:
        clf = pickle.load(f)
    return clf
    
    
def identify(clf, record):
    """
    功能：输入文档向量，判定恶意性
    输入：
        record: 一个文档的向量值
    输出：
        文档的恶意性
    """
    
    record = map(float, record)
    try:
        record = np.array([record])
    except:
        raise TypeError("Record cannot be converted to vectors!\n")

    try:
        result = clf.predict(record)
    except:
        print 'Can not predict!\n'
        raise
        
    if result == 1.0:
        return BAD
    else:
        return GOOD
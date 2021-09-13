#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import numpy as np
import os

from configMgr import config

PDF_CLASSIFIER = config.DETECT_MODEL

BAD = True
GOOD = False

def get_pdf_classifier():
    clf = None
    with open(PDF_CLASSIFIER, 'rb') as f:
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
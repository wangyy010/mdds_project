#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a simple file to extract features from pdfs,
and record them in a file
"""

import env
import mdds.detect_engines.pdf.lib.get_pdf_features as gpf
from mdds.lib.fileType import get_type
import os
import sys
import glob
import traceback

'''
def main(files, des):
    for file in files:
        try:
            records = gpf.get_pdf_features(file)
            gpf.record_features_to_file(records, des)
        except:
            traceback.print_exc()
'''

### RAISE_FILE = r'F:\MyFinalWork\Samples\Raise_Error_Samples\cve_2013_0640'
            
def main(dir, des):
    for root, dirs, files in os.walk(dir):
        for file in files:
            filename = os.path.join(root, file)
            print 'check file: %s' %(filename)
            ### gpf.pdf.logging.debug('check file: %s' %(filename))
            try:
                file_type, data = get_type(filename)
                records = gpf.get_pdf_features(data, filename)
                gpf.record_features_to_file(records, des)
            except:
                traceback.print_exc()
                print 'pdf: %s error' %(filename)
                ### gpf.pdf.logging.debug('pdf: %s error' %(filename))
                raise
                ### raise_file = os.path.join(RAISE_FILE, file)
                ### os.rename(filename, raise_file)
            
            
if __name__ == '__main__':
    sour_dir = sys.argv[1]
    des = sys.argv[2]
    main(sour_dir, des)
    '''
    if os.path.isdir(sour_dir):
        main(glob.glob(sour_dir+'\\*'), des)
    elif os.path.isfile(sour_dir):
        main(glob.glob(sour_dir), des)
    else:
        print sour_dir
    '''
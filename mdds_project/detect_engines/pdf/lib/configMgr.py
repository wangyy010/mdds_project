#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import ConfigParser
import os
import platform
import sys

os_platform = platform.system().lower()
 
DIR = os.path.dirname
ABSPATH = os.path.abspath(__file__)
ROOT = DIR(DIR(ABSPATH))


# ToDo: use __attr__ to replace hard-coded config fields
class configMgr:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        if os_platform == 'windows':
            # print(ROOT)
            path, filename = os.path.split(os.path.realpath(sys.argv[0]))
            self.cf.read(path+r'\config\config.ini')
            # ROOT = self.cf.get("enginespath", "pdf") # for pyinstaller
            ROOT = DIR(DIR(ABSPATH))  # for debug
            self.config_file_path = ROOT + r'\config\config.ini'
            self.cf.read(self.config_file_path)
            # print(os.path.exists(self.config_file_path))
            self.DETECT_MODEL = ROOT + self.cf.get('model', 'detect_model')
            self.LEAF_FILE  = ROOT + self.cf.get('nodes', 'LEAF_FILE')
            self.NODE_FILE  = ROOT + self.cf.get('nodes', 'NODE_FILE')
            self.OPENACTION_FILE = ROOT + self.cf.get('nodes', 'OPENACTION_FILE')
            self.OUTLINES_FILE = ROOT + self.cf.get('nodes', 'OUTLINES_FILE')
            self.PAGE_FILE = ROOT + self.cf.get('nodes', 'PAGE_FILE')
            self.PAGES_FILE = ROOT + self.cf.get('nodes', 'PAGES_FILE')
            self.ROOT_FILE = ROOT + self.cf.get('nodes', 'ROOT_FILE')
            self.TRAILER_FILE = ROOT + self.cf.get('nodes', 'TRAILER_FILE')
        else:
            path, filename = os.path.split(os.path.realpath(sys.argv[0]))
            self.cf.read(os.path.join(path,"config","config.ini")) #"config.ini")
            ROOT = self.cf.get("enginespath", "pdf")
            self.config_file_path = os.path.join(ROOT, "config", "config.ini")#ROOT + r'/config/config.ini'
            self.cf.read(self.config_file_path)
            self.DETECT_MODEL = ROOT + self.cf.get('model', 'detect_model').replace('\\', '/')
            self.LEAF_FILE  = ROOT + self.cf.get('nodes', 'LEAF_FILE').replace('\\', '/')
            self.NODE_FILE  = ROOT + self.cf.get('nodes', 'NODE_FILE').replace('\\', '/')
            self.OPENACTION_FILE = ROOT + self.cf.get('nodes', 'OPENACTION_FILE').replace('\\', '/')
            self.OUTLINES_FILE = ROOT + self.cf.get('nodes', 'OUTLINES_FILE').replace('\\', '/')
            self.PAGE_FILE = ROOT + self.cf.get('nodes', 'PAGE_FILE').replace('\\', '/')
            self.PAGES_FILE = ROOT + self.cf.get('nodes', 'PAGES_FILE').replace('\\', '/')
            self.ROOT_FILE = ROOT + self.cf.get('nodes', 'ROOT_FILE').replace('\\', '/')
            self.TRAILER_FILE = ROOT + self.cf.get('nodes', 'TRAILER_FILE').replace('\\', '/')

            
    def set_attr(self, section, option, value):
        self.cf.set(section, option, value)
        fout = open(self.config_file_path,'w')
        self.cf.write(fout)
        fout.close()

        
config = configMgr()


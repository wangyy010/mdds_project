#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import ConfigParser
import os
import platform
import sys
os_platform = platform.system().lower()
 
DIR = os.path.dirname
ABSPATH = os.path.abspath(__file__)
ROOT = DIR(ABSPATH)


# ToDo: use __attr__ to replace hard-coded config fields
class configMgr:
    def __init__(self):
        self.cf = ConfigParser.ConfigParser()
        if os_platform == 'windows':
            path, filename = os.path.split(os.path.realpath(sys.argv[0]))
            self.cf.read(os.path.join(path,"config","config.ini"))#path+r'\config\config.ini'
            # ROOT = self.cf.get("enginespath", "docx")  # for pyinstaller
            ROOT = DIR(ABSPATH) # for debug
            self.config_file_path = os.path.join(ROOT, "config", "config.ini")#ROOT + r'\config\config.ini'
            self.cf.read(self.config_file_path)
            self.DETECT_MODEL = ROOT + self.cf.get('model', 'detect_model')
            #self.DETECT_MODEL = os.path.join(ROOT, self.cf.get('model', 'detect_model'))#ROOT + self.cf.get('model', 'detect_model')
            self.XML_FEATURE = ROOT + self.cf.get('nodes', 'XML_FEATURE')
            #self.XML_FEATURE  = os.path.join(ROOT, self.cf.get('nodes', 'XML_FEATURE'))#ROOT + self.cf.get('nodes', 'XML_FEATURE')
        else:
            path, filename = os.path.split(os.path.realpath(sys.argv[0]))
            self.cf.read(os.path.join(path,"config","config.ini"))
            ROOT = self.cf.get("enginespath", "docx")
            self.config_file_path = os.path.join(ROOT, "config", "config.ini")
            self.cf.read(self.config_file_path)
            self.DETECT_MODEL = ROOT + self.cf.get('model', 'detect_model').replace('\\', '/')
            self.XML_FEATURE  = ROOT + self.cf.get('nodes', 'XML_FEATURE').replace('\\', '/')


            
    def set_attr(self, section, option, value):
        self.cf.set(section, option, value)
        fout = open(self.config_file_path,'w')
        self.cf.write(fout)
        fout.close()

        
config = configMgr()


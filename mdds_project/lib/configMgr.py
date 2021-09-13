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
            self.config_file_path = ROOT + r'\config\config.ini' 
            self.cf.read(self.config_file_path)
            self.DATABASE = ROOT + self.cf.get('database', 'DATABASE')
            self.log_path = ROOT + self.cf.get('log', 'log_path')
            self.thread_num = self.cf.get('multi_thread', 'thread_num')

        '''
        
        else:
            self.config_file_path = ROOT + r'/config/config.ini'
            self.cf.read(self.config_file_path)
            self.DATABASE =ROOT + r'\database\database.db'.replace('\\', '/')
            self.log_path = ROOT  + r'\log\log.txt'.replace('\\', '/')
        '''


        
        
    def set_attr(self, section, option, value):
        self.cf.set(section, option, value)
        fout = open(self.config_file_path,'w')
        self.cf.write(fout)
        fout.close()

        
config = configMgr()


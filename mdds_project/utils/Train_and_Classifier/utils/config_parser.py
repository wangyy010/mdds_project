#!/usr/bin/env python
# -*- coding: utf-8 -*-

# parse and generate the global configuration
import os

# The ConfigParser class should be singleton
# There may be more elegant way to implement singleton in Python
# http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python/33201#33201

LOG_DIR = 'log-directory'

class Singleton(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    
class ConfigParser(Singleton):
    logDir = None
    threadsNum = 1
    
    directories = {LOG_DIR: logDir}
        
    def parseFile(self, filePath):
        if filePath and os.path.exists(filePath):
            try:
                fileObj = open(filePath, 'r')
            except IOError,e:
                print e
            try:
                lines = fileObj.readlines()
                if lines:
                    self.parseStreams(lines)
            except IOError,e:
                print e
            finally:
                fileObj.close()
                
    def parseStreams(self, lines):
        for line in lines:
            if line.startswith('#') or line == os.linesep:
                continue
            else:
                elems = line.split('=')
                elems = [elem.strip() for elem in elems]
                paramKey = elems[0]
                paramValue = elems[-1]
                if paramKey == 'LOG_DIR':
	            self.directories[LOG_DIR] = self.logDir = paramValue
                else:
                    continue
                
        self.generateDirectories()
              
    # generate all the directories if needed
    def generateDirectories(self):
        for directory in self.directories.values():
            if not os.path.exists(directory):
                try:
                    os.makedirs(directory)
                except OSError,e:
                    print e
                    
    
    def getLogDir(self):
        return self.logDir
    


    
if __name__ == '__main__':
    path = '/home/songlee/codes/myVModel.ini'
    configParser = ConfigParser()
    configParser.parseFile(path)
    print configParser.getLogDir()
    configParser.generateDirectories()
    print configParser.getLogDir()

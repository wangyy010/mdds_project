#!/usr/bin/python

import vbaDocx
import oleDocx
import sys
import os
import operator
import re
import zipfile
import xml_feature
import olevba
from thirdparty import olefile
import msodde


LOCATIONS = ['document.xml','endnotes.xml','footnotes.xml','header1.xml',
             'footer1.xml','header2.xml','footer2.xml','comments.xml']


from configMgr import config
XML_FEATURE = config.XML_FEATURE

class xml_parser(olevba.VBA_Parser_CLI):

    def __init__(self, *args, **kwargs):
        super(xml_parser, self).__init__(*args, **kwargs)


    def get_xml_dde(self):

        res = ''
        res += msodde.process_file(self.filename)
        return res




    def get_xml_feature(self):
        node = {}
        outputfile = open(XML_FEATURE,'r')
        dict = {}
        for line in outputfile:
            line = line.replace('\n','')
            if not dict.has_key(line):
                dict[line] = 0

        #sort_dict = sorted(dict.keys())
        #print dict
        with zipfile.ZipFile(self.filename, 'r') as fr:
            for subfile in fr.namelist():
                if os.path.splitext(subfile)[1] == '.xml':
                    f = subfile.split('/')

                    if len(f) == 1:
                        f = f[0] + '\\'
                    elif len(f) == 2:
                        f = f[0] + '\\' + f[1] + '\\'
                    elif len(f) == 3:
                        f = f[0] + '\\' + f[1] + '\\' + f[2] + '\\'

                    xml = fr.open(subfile).read()
                    res = OfficeNode(f, xml)
                    for i in res.result:
                        if i in dict.keys():
                            dict[i] = 1
        outputfile.close()
        result = ''
        for key in sorted(dict.keys()):
            result += str(dict[key])
        res = ''
        for i in result:
            res += i + ','
        res = res[:-1]
        res = res + '\n'
        return res


class OfficeNode:

    def __init__(self, result,xml=None):

        self.indata = xml
        self.result = [result]
        if xml:
            self.dict_xml = xml_feature.parse(self.indata)
            self.__myParseTag(self.dict_xml, result)
            #print self.result
    def __myParseTag(self, dict_xml, parent_path):
        for key in dict_xml.keys():
            current_path = parent_path + str(key) + '\\' + ''
            if not re.findall(r'@', key):
                self.result.append(current_path)
            else:
                continue
            val = dict_xml[key]
            if isinstance(val, dict):
                self.__myParseTag(val, current_path)
            elif isinstance(val, list):
                for v in val:
                    if isinstance(v, dict):
                        self.__myParseTag(v, current_path)








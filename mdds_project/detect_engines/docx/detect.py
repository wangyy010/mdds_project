#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

import classifier
import extractFeature
import oleDocx
import xmlDocx
import vbaDocx
import olevba


def detect(data, filename):

    try:
        ole_parser = oleDocx.ole_parser(filename)
        xml_parser = xmlDocx.xml_parser(filename)
        vba_parser = vbaDocx.vba_parser(filename)
        analysis = extractFeature.OfficeFeatureExtractor(filename)
        vba_code = vba_parser.get_vba()
        ole_code = ole_parser.get_ole()
        xml_code = xml_parser.get_xml_dde()
        all_code = str(vba_code) + xml_code.encode('utf-8') + ole_code
        vector = analysis.print_analysis(all_code)
        vector = vector.replace(',','').strip('\n')
        list = []
        for i in vector:
            list.append(int(i))
        clf = classifier.get_docx_classifier()
        result = classifier.identify(clf,list)
    except:
        raise
    return result

def describe(filename):

    try:
        ole_parser = oleDocx.ole_parser(filename)
        xml_parser = xmlDocx.xml_parser(filename)
        vba_parser = vbaDocx.vba_parser(filename)
        analysis = extractFeature.OfficeFeatureExtractor(filename)
        vba_code = vba_parser.get_vba()
        ole_code = ole_parser.get_ole()
        xml_code = xml_parser.get_xml_dde()
        all_code = str(vba_code) + xml_code.encode('utf-8') + ole_code
        vector = analysis.print_analysis(all_code)
        vector = vector.replace(',', '').strip('\n')
        list = []
        for i in vector:
            list.append(int(i))
        result = analysis.showResults(all_code)
        '''
        for i in range(13):
            if list[i] != 0:
                result = result + 'AutoExec' + ';'
                break
        if list[13] == 3:
            result = result + 'More IOC' + ';'
        elif list[13] == 2:
            result = result + 'Less IOC' + ';'
        for i in range(14,122):
            if list[i] != 0:
                result = result + 'Suspicious' + ';'
                break
        '''

        if list[122] == 2:
            result = result + 'Longer Confused String' + '\n'
        elif list[122] == 1:
            result = result + 'Confused String' + '\n'
        if list[123] == 3:
            result = result + 'More Confused Strings' + '\n'
        elif list[123] == 2:
            result = result + 'Less Confused Strings' + '\n'
        if list[124] == 1:
            result = result + 'The Strings has function name' + '\n'
        if list[125] == 3:
            result = result + 'More long function name' + '\n'
        elif list[125] == 2:
            result = result + 'Less long function name' + '\n'
        if list[126] == 3:
            result = result + 'More long Strings' + '\n'
        elif list[126] == 2:
            result = result + 'Less long Strings' + '\n'
        if list[127] == 3:
            result = result + 'More long var' + '\n'
        elif list[127] == 2:
            result = result + 'Less long var' + '\n'
        if list[128] == 1:
            result = result + 'More circulation' + '\n'
        if list[129] == 1:
            result = result + 'More Compare' + '\n'
        if list[130] == 1:
            result = result + 'More Calculate' + '\n'
        if list[131] == 3:
            result = result + 'More plus signs in Strings' + '\n'
        elif list[131] == 2:
            result = result + 'Less plus signs in Strings ' + '\n'


    except:
        raise
    return result

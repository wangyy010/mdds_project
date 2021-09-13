#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

import env
import detect_engines.pdf.lib.classifier as classifier
import detect_engines.pdf.lib.get_pdf_features as gpf


def detect(data, filename):
    try:
        vector = gpf.get_pdf_features(data, filename)
        clf = classifier.get_pdf_classifier()
        result = classifier.identify(clf, vector)
    except:
        raise
    return result


def describe(data, filename):
    result = ''
    try:
        vector = gpf.get_pdf_features(data, filename)
        if int(vector[296]) == 2:
            result += 'Long Annotation Length\n'
        if int(vector[298]) == 2:
            result += 'Long Confused String\n'
        if int(vector[299]) == 2:
            result += 'Multi Confused Strings\n'
        if int(vector[299]) == 1:
            result += 'Few Confused Strings\n'
        if int(vector[300]) == 1:
            result += 'Function Name in Strings\n'
        if int(vector[301]) == 1:
            result += 'Out Reference\n'
        if int(vector[302]) == 2:
            result += 'Multi Long Name Functions\n'
        if int(vector[302]) == 1:
            result += 'Few Long Name Functions\n'
        if int(vector[303]) == 2:
            result += 'Multi Long Strings\n'
        if int(vector[303]) == 1:
            result += 'Few Long Strings\n'
        if int(vector[304]) == 2:
            result += 'Multi Long Name Var\n'
        if int(vector[304]) == 1:
            result += 'Few Long Name Var\n'
        if int(vector[305]) == 2 or int(vector[305]) == 1:
            result += 'Multi \'+\' in Strings\n'
        if int(vector[306]) > 0:
            result += 'Suspicious Api \'app\'\n'
        if int(vector[307]) > 0:
            result += 'Suspicious Api \'apply\'\n'
        if int(vector[308]) > 0:
            result += 'Suspicious Api \'charCodeAt\'\n'
        if int(vector[309]) > 0:
            result += 'Suspicious Api \'concat\'\n'
        if int(vector[310]) > 0:
            result += 'Suspicious Api \'Date\'\n'
        if int(vector[311]) > 0:
            result += 'Suspicious Api \'doc\'\n'
        if int(vector[312]) > 0:
            result += 'Suspicious Api \'escape\'\n'
        if int(vector[313]) > 0:
            result += 'Suspicious Api \'eval\'\n'
        if int(vector[314]) > 0:
            result += 'Suspicious Api \'execInitializ\'\n'
        if int(vector[315]) > 0:
            result += 'Suspicious Key Word \'for\'\n'
        if int(vector[316]) > 0:
            result += 'Suspicious Api \'fromCharCode\'\n'
        if int(vector[317]) > 0:
            result += 'Suspicious Api \'function\'\n'
        if int(vector[318]) > 0:
            result += 'Suspicious Api \'join\'\n'
        if int(vector[319]) > 0:
            result += 'Suspicious Api \'getAnnots\'\n'
        if int(vector[320]) > 0:
            result += 'Suspicious Api \'length\'\n'
        if int(vector[321]) > 0:
            result += 'Suspicious Api \'new\'\n'
        if int(vector[322]) > 0:
            result += 'Suspicious Api \'push\'\n'
        if int(vector[323]) > 0:
            result += 'Suspicious Api \'rawValue\'\n'
        if int(vector[324]) > 0:
            result += 'Suspicious Api \'replace\'\n'
        if int(vector[325]) > 0:
            result += 'Suspicious Api \'search\'\n'
        if int(vector[326]) > 0:
            result += 'Suspicious Api \'String\'\n'
        if int(vector[327]) > 0:
            result += 'Suspicious Api \'substr\'\n'
        if int(vector[328]) > 0:
            result += 'Suspicious Api \'splite\'\n'
        if int(vector[329]) > 0:
            result += 'Suspicious Api \'syncAnnotScan\'\n'
        if int(vector[330]) > 0:
            result += 'Suspicious Api \'target\'\n'
        if int(vector[331]) > 0:
            result += 'Suspicious Key Word \'this\'\n'
        if int(vector[332]) > 0:
            result += 'Suspicious Api \'toLowerCase\'\n'
        if int(vector[333]) > 0:
            result += 'Suspicious Api \'toUpperCase\'\n'
        if int(vector[334]) > 0:
            result += 'Suspicious Api \'util.printf\'\n'
        if int(vector[335]) > 0:
            result += 'Suspicious Api \'unescape\'\n'
        if int(vector[336]) > 0:
            result += 'Suspicious Key Word \'while\'\n'

        return result
    except:
        raise


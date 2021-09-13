#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

PDF  = 0x00
DOC  = 0X01
DOCX = 0X02
PPT  = 0X03
PPTX = 0X04
XLS  = 0X05
XLSX = 0X06
RIFF = 0X07
NC   = 0X08
OLE  = 0X09
ZIP  = 0X0A
RAR  = 0X0B
ISO  = 0X0C
FLA  = 0X0D
WAV  = 0X0E
MP3  = 0X0F
PNG  = 0X10
JPG  = 0X11
JPEG = 0X12
BMP  = 0X13
WPS  = 0X14
HTML = 0X15
XML  = 0X16
TXT  = 0x17
CPP  = 0x18

UNKNOW = 0x19

def get_data(filename):
    data = None
    with open(filename, 'rb') as f:
        data = f.read()
    return data

# ========= Level One =========== #    

def be_pdf(data):
    pos = data[0:1024].find('%PDF-')
    if pos >= 0 and pos <= 1024:
        return True
    return False

    
def be_zip(filename):
    import zipfile
    return zipfile.is_zipfile(filename)
    
    
def be_ole(data):
    #if len(data) <= 1427: return False
    return data[0:8] == '\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1'
    
    
def be_rar(data):
    return False
    
    
def be_iso(data):
    return False
    
    
def be_wav(data):
    return False

    
def be_riff(data):
    return False
    
    
def be_mp3(data):
    return False
    
    
def be_png(data):
    return False

    
def be_jpeg(data):
    return False

    
def be_jpg(data):
    return False
   
   
def be_bmp(data):
    return False
   
   
def be_nc(data):
    return False    
   
   
def be_html(data):
    return False
    
    
def be_xml(data):
    return False
    
    
def be_cpp(data):
    return False    
    
    
def be_txt(filename):
    return False
    
# ========= Level Two =========== #    

def be_docx(data):
    import re
    if len(data) <= 67: return False
    temp = re.findall(r'\[Content_Types\]\.xml|_rels/\.rels',data)
    if temp:
        if re.findall(r'word\/',data):
            return True
    return False



def be_pptx(data):
    import re
    if len(data) <= 67: return False
    temp = re.findall(r'\[Content_Types\]\.xml|_rels/\.rels', data)
    if temp:
        if re.findall(r'ppt\/', data):
            return True
    return False

def be_xlsx(data):
    return False

def be_doc(data):
    return data[546:550] == '\x62\x6a\x62\x6a'

    
def be_ppt(data):
    return False
    #return data[1408:1428] == '\x50\x00\x6f\x00\x77\x00\x65\x00\x72\x00\x50\x00\x6f\x00\x69\x00\x6e\x00\x74\x00'
    
    
def be_xls(data):
    return False
    
    
def be_wps(data):
    return False
    
    
def be_fla(data):
    return False

    
# =========== API ========= #
    
def get_type(filename):
    data = get_data(filename)
    type = UNKNOW
    if data:
        if be_pdf(data):
            type = PDF
        elif be_ole(data):
            if be_doc(data):
                type = DOC
            elif be_ppt(data):
                type = PPT
            elif be_xls(data):
                type = XLS
            elif be_fla(data):
                type = FLA
            elif be_wps(data):
                type = WPS
            else:
                type = OLE
        elif be_zip(filename):
            if be_docx(data):
                type = DOCX
            elif be_pptx(data):
                type = PPTX
            elif be_xlsx(data):
                type = XLSX
            else:
                type = ZIP
        elif be_rar(data):
            type = RAR
        elif be_iso(data):
            type = ISO
        elif be_wav(data):
            type = WAV
        elif be_riff(data):
            type = RIFF
        elif be_mp3(data):
            type = MP3
        elif be_png(data):
            type = PNG
        elif be_jpeg(data):
            type = JPEG
        elif be_jpg(data):
            type = JPG
        elif be_bmp(data):
            type = BMP
        elif be_nc(data):
            type = NC
        elif be_html(data):
            type = HTML
        elif be_xml(data):
            type = XML
        elif be_cpp(data):
            type = CPP
        elif be_txt(filename):
            type = TXT
    
    return type, data
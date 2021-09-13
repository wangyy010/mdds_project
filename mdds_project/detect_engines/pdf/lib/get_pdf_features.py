#!/usr/bin/env python
# -*- coding: utf-8 -*-

import env
import pdf
import re
import exceptions
import os

# ++++++++++++++ 设置配置信息 ++++++++++++++
from configMgr import config

LEAF_FILE = config.LEAF_FILE
NODE_FILE = config.NODE_FILE
OPENACTION_FILE = config.OPENACTION_FILE
OUTLINES_FILE = config.OUTLINES_FILE
PAGE_FILE = config.PAGE_FILE
PAGES_FILE = config.PAGES_FILE
ROOT_FILE = config.ROOT_FILE
TRAILER_FILE = config.TRAILER_FILE


def read_features_from_file(filename):
    """
    元数据特征都写到txt文件里了
    """
    with open(filename, 'r') as fr:
        datas = fr.readlines()
    result = []
    for keyword in datas:
        result.append(keyword.strip('\n'))
    return result
    
    
# +++++++++++++++++++++ Classes +++++++++++++++++++++
    
class ObjFeature:
    """
    record the features of every pdf obj
    """
    
    LONG_VAR = 10 # 变量名阈值
    LONG_FUNC = 10 # 函数名阈值
    LONG_STR = 50 # 字符串阈值
    PLUS_COUNT = 2 # 一个字符串中'+'出现的阈值
    SUSPICIOUS_APIS = [ 'app', 'apply', 'charCodeAt', 'concat', 'Date',
                        'doc', 'escape', 'eval', 'execInitialize', 'for',
                        'fromCharCode', 'function', 'join', 'getAnnots', 'length',
                        'new', 'push', 'rawValue', 'replace', 'search', 
                        'rawValue', 'String', 'substr', 'splite', 'syncAnnotScan', 
                        'target', 'this', 'toLowerCase', 'toUpperCase', 'util.printf', 
                        'unescape', 'while' 
                      ]


    def __init__(self, obj=pdf.pdfobj('0 0')):
        self.__obj = obj
        self.keynum = obj.keynum ####临时这样写了，以后要好好修改analyze_js函数为static
        self.tags = obj.tags
        self.Kids = set()
        self.type = 'UNKNOW' # should be ['Root', 'Pages', 'Page', 'Node', 'Leaf', 'OpenAction', 'Xref', 'Trailer']
        self.has_hidden_tags = False
        self.has_embedded_file = False
        # key words features
        self.has_kw_OpenAction = False
        self.has_kw_JS = False
        self.has_kw_JavaScript = False
        self.has_kw_Action = False
        self.has_kw_S = False
        self.has_kw_PageMode = False
        self.has_kw_Outlines = False
        self.has_kw_AA = False
        self.has_kw_URI = False
        # stream features
        self.has_stream = False
        self.stream_real_length = 0
        self.decode_methods = []
        ################################### JS features ######################################
        self.has_js = False # 是否有js代码
        self.js_code = '' # 解压后的js代码
        self.has_annotation = False # 有注释
        self.annotation_num = 0
        self.annotation_length = 0
        self.has_long_var = False # 变量名很长
        self.long_var_num = 0
        self.has_long_func_name = False #函数名很长
        self.long_func_num = 0
        self.has_long_str = False # 有很长的字符串
        self.long_str_num = 0
        self.has_confused_str = False # 字符串使用不常见编码
        self.confused_str_num = 0
        self.confused_str_length = 0
        self.suspicious_api = {} # 记录出现的可疑api和出现的次数
        self.multi_plus_str = 0 # 含有多个'+'的字符串数量
        self.funcs_in_str = {} # 记录函数名出现在长字符串中func:num
        self.has_Annot = False
        ####
        self.__parse_obj()
        
        
    def __parse_obj(self):
        """
        解析obj基本信息，为提取特征做条件准备，
        我认为get_js_feature最好在PdfFeatureExtractor去实现，由于时间关系以后再做修改
        """
        self.__get_kids()
        self.__get_type()
        self.__get_has_hidden_tags()
        self.__get_has_embedded_file()
        self.__get_stream_features()
        self.__get_js_features()

        
    def __get_kids(self):
        for tag, kid in self.__obj.children:
            self.Kids.add(kid)
            
        for tag, kid in self.__obj.Kids:
            self.Kids.add(kid)
        
        for tag, kid in self.__obj.xfaChildren:
            self.Kids.add(kid)

            
    def __get_type(self):
        if self.__obj.type: # 如果在外部已经对obj的类型进行了判定，查阅pdf.py line:851
            self.type = self.__obj.type
        elif self.keynum == 'trailer':
            self.type = 'Trailer'
        elif self.keynum == 'xref':
            self.type = 'Xref'
        else:
            for kstate, k, kval in self.__obj.tags:
                if 'Pages' == k and kval == '':
                    self.type = 'Pages'
                    return self.type
            for kstate, k, kval in self.__obj.tags:
                if 'Page' == k and kval == '':
                    self.type = 'Page'
                    return self.type
            if self.Kids:
                self.type = 'Node'
            else:
                self.type = 'Leaf'
        return self.type

        
    def __get_has_hidden_tags(self):
        if self.__obj.hiddenTags:
            self.has_hidden_tags = True

            
    def __get_has_embedded_file(self):
        self.has_embedded_file = self.__obj.isEmbedded

        
    def __get_stream_features(self):
        """
        读取stream的长度、编码方式
        """
        if self.__obj.tagstream:
            self.has_stream = True
            self.stream_real_length = len(self.__obj.tagstream)
            for kstate, k, kval in self.__obj.tags:                    
                if k == 'Filter':
                    kval = pdf.pdfobj.fixPound(kval)
                    self.decode_methods = re.findall('/(\w+)', kval)

                    
    def __get_js_features(self):
        self.has_js = self.__obj.isJS
        if self.has_js:
            self.js_code = self.__obj.tagstream
            self.__analyze_js(self.js_code)

            
    def __analyze_js(self, js_code):
        # 注释
        annotations = re.findall(r'/\*(.*?)\*/', js_code, re.MULTILINE | re.DOTALL)
        for annotation in annotations:
            self.annotation_num += 1
            self.annotation_length += len(annotation)
        self.has_annotation = self.annotation_num > 0
            
        # 去掉注释
        clean_code = re.sub(r'/\*.*?\*/', '', js_code)
            
        # 长变量名
        vars = re.findall(r'var\s+([_a-zA-Z]?[a-zA-Z]+[0-9]*[a-zA-Z]*)\s*=\s*.*?', clean_code, re.MULTILINE | re.DOTALL)
        for var in vars:
            if len(var) > ObjFeature.LONG_VAR:
                self.long_var_num += 1
        self.has_long_var = self.long_var_num > 0
            
        # 长函数名
        funcs = re.findall(r'function\s+([_a-zA-Z]?[a-zA-Z]+[0-9]*[a-zA-Z]*)\n?\s*.*?', clean_code, re.MULTILINE | re.DOTALL)
        funcs2 = re.findall(r'var\s+([_a-zA-Z]?[a-zA-Z]+[0-9]*[a-zA-Z]*)\s*=\s*\[?\s*function.*?', clean_code, re.MULTILINE | re.DOTALL)
        funcs.extend(funcs2)
        for func_name in funcs:
            if len(func_name) > ObjFeature.LONG_FUNC:
                self.long_func_num += 1
        self.has_long_func_name = self.long_func_num > 0
            
        # 长字符串
        long_strs = re.findall(r'\'(.*?)\'.*?', clean_code, re.MULTILINE | re.DOTALL)
        str2 = re.findall(r'\"(.*?)\".*?', clean_code, re.MULTILINE | re.DOTALL)
        long_strs.extend(str2)
        the_longest_str = ''
        for str in long_strs:
            # 记录最长的str
            if len(str) > len(the_longest_str):
                the_longest_str = str
            # 长字符串数量
            if len(str) > ObjFeature.LONG_STR:
                self.long_str_num += 1
            # 字符串里有特殊编码
            result = None
            result = re.search(r'(\\u[0-9]{2})+.*?', str)
            if result:
                self.confused_str_num += 1
                self.confused_str_length += len(result.group(0))
            result = re.search(r'(\\x[0-9]{2})+.*?', str)
            if result:
                self.confused_str_num += 1
                self.confused_str_length += len(result.group(0))
            # 字符串中含有多个'+'号
            if str.count('+') > ObjFeature.PLUS_COUNT:
                self.multi_plus_str += 1
            # 函数名在长字符串中出现
            for func in funcs:
                if not self.funcs_in_str.has_key(func):
                    self.funcs_in_str[func] = 1
                else:
                    self.funcs_in_str[func] += 1    
        self.has_long_str = self.long_str_num > 0 # 有长字符串
        self.has_confused_str = self.confused_str_length > 0 # 特殊编码字符串的长度
        # 说明需要检测含有tag:'isAnnot'的obj
        if 'Annot' in clean_code:
            self.has_Annot = True
        # 记录可疑api调用次数
        for api in ObjFeature.SUSPICIOUS_APIS:
            self.suspicious_api[api] = clean_code.count(api)
            
            
class PdfFeatureExtractor:
    """
    Feature Extractor for PDF document
    """
    FEW = 2 
    MULTI = 3 
    SHORT = 1 # 注释长度 [0, 50]
    LONG = 2 # 注释长度(50, )
    
    LEAF = []
    NODE = []
    OPENACTION = []
    OUTLINES = []
    PAGE = []
    PAGES = []
    ROOT = []
    TRAILER = []
    HAVE_PREPARED = False # True:已经执行了read_node_features函数
    
    
    @staticmethod
    def read_node_features():
        """
        从txt中读取所有的元数据特征
        """
        PdfFeatureExtractor.LEAF = read_features_from_file(LEAF_FILE)
        PdfFeatureExtractor.NODE = read_features_from_file(NODE_FILE)
        PdfFeatureExtractor.OPENACTION = read_features_from_file(OPENACTION_FILE)
        PdfFeatureExtractor.OUTLINES = read_features_from_file(OUTLINES_FILE)
        PdfFeatureExtractor.PAGE = read_features_from_file(PAGE_FILE)
        PdfFeatureExtractor.PAGES = read_features_from_file(PAGES_FILE)
        PdfFeatureExtractor.ROOT = read_features_from_file(ROOT_FILE)
        PdfFeatureExtractor.TRAILER = read_features_from_file(TRAILER_FILE)
        PdfFeatureExtractor.HAVE_PREPARED = True
    
    
    def __init__(self, data, filename):
        self.LEAF = {}
        self.NODE = {}
        self.OPENACTION = {}
        self.OUTLINES = {}
        self.PAGE = {}
        self.PAGES = {}
        self.ROOT = {}
        self.TRAILER = {}
        self.JS = {}
        self._js_list = []
        self._ObjFeature_list = []
        self._filename = filename
        self._pdf = None
        self.obj_features = {}
        self.js_obj_features = {}
        
        self.prepare_node_features()
        if data == None:
            with open(filename, 'rb') as fin:
                data = fin.read()
        mypdf = pdf.pdf(data, filename, '')
        if mypdf.is_valid():
            self._pdf = mypdf
        else:
            raise TypeError("%s is not a pdf file" % filename)
            
    def prepare_node_features(self):
        """
        初始化各种节点类型的特征
        """
        if not PdfFeatureExtractor.HAVE_PREPARED:
            PdfFeatureExtractor.read_node_features()

        def read_to_dict(list, dict):
            for keyword in list:
                dict[keyword] = 0

        read_to_dict(PdfFeatureExtractor.LEAF, self.LEAF)
        read_to_dict(PdfFeatureExtractor.NODE, self.NODE)
        read_to_dict(PdfFeatureExtractor.OPENACTION, self.OPENACTION)
        read_to_dict(PdfFeatureExtractor.OUTLINES, self.OUTLINES)
        read_to_dict(PdfFeatureExtractor.PAGE, self.PAGE)
        read_to_dict(PdfFeatureExtractor.PAGES, self.PAGES)
        read_to_dict(PdfFeatureExtractor.ROOT, self.ROOT)
        read_to_dict(PdfFeatureExtractor.TRAILER, self.TRAILER)


    def extract_features(self):
        if self._pdf:
            try:
                self._pdf.parse()
            except:
                print ('can not parse the file', self._filename)
                ### pdf.logging.debug('can not parse the file', self._filename)
                raise 
            else:
                self.__parse_every_obj()
                if len(self._js_list) > 0:
                    self.JS = self._js_list[0] # 以后这里需要修改
                else: # 没有js代码
                    self.JS = self.get_js_features(ObjFeature())
                
                
    def __parse_every_obj(self):
        """
        parse every obj and extract the features, 
        this function can only be used after pdf.parse()
        """
        
        for key in self._pdf.objects.keys():
            obj = self._pdf.objects[key]
            obj_feature = ObjFeature(obj)
            self.obj_features[key] = obj_feature
            if obj_feature.has_js:
                self.js_obj_features[key] = obj_feature
        valid_nodes = self.pruning_algorithm()
        for key in valid_nodes:
            obj_feature = self.obj_features[key]
            self.__result_of_obj(obj_feature)
            
            
    def __result_of_obj(self, ObjFeature):
        """
        根据实际obj类型，分类提取不同的features
        """
        
        if ObjFeature.has_js:
            js_result = self.get_js_features(ObjFeature)
            self._js_list.append(js_result)
        
        def parse(tags, dict):
            for kstate, k, kval in tags:
                if k in dict.keys():
                    dict[k] += 1
                    
        dict = {}            
        if ObjFeature.type == 'Leaf':
            dict = self.LEAF
        elif ObjFeature.type == 'Node':
            dict = self.NODE
        elif ObjFeature.type == 'OpenAction':
            dict = self.OPENACTION
        elif ObjFeature.type == 'Outlines':
            dict = self.OUTLINES
        elif ObjFeature.type == 'Page':
            dict = self.PAGE
        elif ObjFeature.type == 'Pages':
            dict = self.PAGES
        elif ObjFeature.type == 'Root':
            dict = self.ROOT
        elif ObjFeature.type == 'Trailer':
            dict = self.TRAILER
        parse(ObjFeature.tags, dict)
        
        
    def get_root_id(self):
        for id in self._pdf.objects.keys():
            if self.obj_features[id].type == "Root":
                return id
        return None
        
    
    def breadth_first_travel(self, root_id):
        """
        This is designed for the PDF which not contains JavaScript code
        """
        # from queue import Queue
        import Queue
        q = Queue.Queue()
        valid_nodes = []
        
        s = set()
        q.put(root_id)
        while not q.empty():
            id = q.get()
            if id not in s: # 防止形成环
                s.add(id)
                valid_nodes.append(id)
                obj_feature = self.obj_features[id]
                for node in obj_feature.Kids:
                    if node in self.obj_features.keys():
                        q.put(node)
                    else:
                        pass # 说明PDF有解析错误
        return valid_nodes
        
        
    def depth_first_travel(self, root_id, depth_level = 1):
        """
        This is designed for the PDF which contains JavaScript codes.
        """
        stack = [] # Use list as a stack, record the current path
        valid_nodes = []
        self.depth_first_travel_core(root_id, stack, valid_nodes)
        self.depth_level_travel(valid_nodes, depth_level)
        return valid_nodes
    
    
    def depth_first_travel_core(self, kid, stack, valid_nodes):
        if kid in stack: # 防止形成环
            return
        stack.append(kid)
        if kid in self.js_obj_features.keys():
            for node in stack:
                if node not in valid_nodes:
                    valid_nodes.append(node)
        else:
            for child in self.obj_features[kid].Kids:
                if child in self.obj_features.keys(): # 防止PDF文档解析错误
                    self.depth_first_travel_core(child, stack, valid_nodes)
                else:
                    pass # 说明PDF有解析错误
        stack.pop()
     
    
    def depth_level_travel(self, valid_nodes, depth_level = 1):
        if depth_level:
            for node in valid_nodes:
                for kid in self.obj_features[node].Kids:
                    if kid not in valid_nodes and kid in self.obj_features.keys():
                        valid_nodes.append(kid)
            self.depth_level_travel(valid_nodes, depth_level-1)
     
        
    def pruning_algorithm(self):
        valid_nodes = []
        root_id = self.get_root_id()
        if root_id:
            if self.js_obj_features.keys() == []:
                valid_nodes = self.breadth_first_travel(root_id)
            else:
                valid_nodes = self.depth_first_travel(root_id)
        else:
            valid_nodes = self.obj_features.keys()
        return valid_nodes
        
    
    def get_js_features(self, ObjFeature):
        """
        可供外部使用
        目前主要是获得js代码的特征，具体特征如下：
        result = {
                    'has_annotation' : 0 # 有注释
                    'annotation_num' : 0 # 注释数量
                    'annotation_length' : 0 # 注释长度
                    'has_long_var' : 0 # 变量名很长
                    'long_var_num' : 0
                    'has_long_func_name' : 0 #函数名很长
                    'long_func_num' : 0
                    'has_long_str' : 0 # 有很长的字符串
                    'long_str_num' : 0
                    'has_confused_str' : 0 # 字符串使用不常见编码
                    'confused_str_num' : 0
                    'confused_str_length' : 0
                    'suspicious_api' : {} # 记录出现的可疑api和出现的次数
                    'multi_plus_str' : 0 # 含有多个'+'的字符串数量
                    'funcs_in_str' : 0 # 记录函数名出现在长字符串中func:num
                    'has_Annot' : 0 # 有向外的引用 （以后这里需要做 扩充 ）
                }
        result中的suspicious_api具体内容如下：
        suspicious_api = {
                            'app' : 0
                            'apply' : 0
                            'charCodeAt' : 0
                            'concat' : 0
                            'Date' : 0
                            'doc' : 0
                            'eval' : 0
                            'execInitialize' : 0
                            'for' : 0
                            'fromCharCode' : 0
                            'function' : 0
                            'join' : 0 
                            'getAnnots' : 0
                            'length' : 0 
                            'new' : 0
                            'push' : 0 
                            'rawValue' : 0
                            'replace' : 0
                            'search' : 0 
                            'rawValue' : 0
                            'String' : 0 
                            'substr' : 0 
                            'splite' : 0 
                            'syncAnnotScan' : 0 
                            'target' : 0
                            'this' : 0 
                            'toLowerCase' : 0 
                            'toUpperCase' : 0 
                            'util.printf' : 0 
                            'unescape' : 0
                            'while' : 0
                         }
        """
        # 初始化 suspicious_api #
        suspicious_api = {
                            'app' : 0,
                            'apply' : 0,
                            'charCodeAt' : 0,
                            'concat' : 0,
                            'Date' : 0,
                            'doc' : 0,
                            'escape' : 0,
                            'eval' : 0,
                            'execInitialize' : 0,
                            'for' : 0,
                            'fromCharCode' : 0,
                            'function' : 0,
                            'join' : 0 ,
                            'getAnnots' : 0,
                            'length' : 0,
                            'new' : 0,
                            'push' : 0,
                            'rawValue' : 0,
                            'replace' : 0,
                            'search' : 0,
                            'rawValue' : 0,
                            'String' : 0,
                            'substr' : 0,
                            'splite' : 0,
                            'syncAnnotScan' : 0, 
                            'target' : 0,
                            'this' : 0,
                            'toLowerCase' : 0, 
                            'toUpperCase' : 0,
                            'util.printf' : 0,
                            'unescape' : 0,
                            'while' : 0
                         }
        
        result = {
                    # 'has_annotation' : 0, # 有注释
                    'annotation_num' : 0, # 注释数量
                    'annotation_length' : 0, # 注释长度
                    # 'has_long_var' : 0, # 变量名很长
                    'long_var_num' : 0,
                    # 'has_long_func_name' : 0, #函数名很长
                    'long_func_num' : 0,
                    # 'has_long_str' : 0, # 有很长的字符串
                    'long_str_num' : 0,
                    # 'has_confused_str' : 0, # 字符串使用不常见编码
                    'confused_str_num' : 0,
                    'confused_str_length' : 0,
                    'suspicious_api' : suspicious_api, # 记录出现的可疑api和出现的次数
                    'multi_plus_str' : 0, # 含有多个'+'的字符串数量
                    'funcs_in_str' : 0, # 记录函数名出现在长字符串中func:num
                    'has_Annot' : 0 # 有向外的引用 （以后这里需要做 扩充 ）
                }
        
        # 真正的数据 #
        # result['has_annotation'] = 1 if ObjFeature.has_annotation else 0 # 有注释
        # 注释数量
        if ObjFeature.annotation_num > 0:
            result['annotation_num'] = PdfFeatureExtractor.FEW
        # 注释长度
        if ObjFeature.annotation_length > 50:
            result['annotation_length'] = PdfFeatureExtractor.LONG
        elif ObjFeature.annotation_length >= 1:
            result['annotation_length'] = PdfFeatureExtractor.SHORT
        else:
            result['annotation_length'] = ObjFeature.annotation_length
        # 有长变量名
        # result['has_long_var'] = 1 if ObjFeature.has_long_var else 0
        # 长变量名数量
        if ObjFeature.long_var_num > 5:
            result['long_var_num'] = PdfFeatureExtractor.MULTI
        elif ObjFeature.long_var_num > 1:
            result['long_var_num'] = PdfFeatureExtractor.FEW
        else:
            result['long_var_num'] = ObjFeature.long_var_num
        # 含有长函数名
        # result['has_long_func_name'] = 1 if ObjFeature.has_long_func_name else 0
        # 长函数名数量
        if ObjFeature.long_func_num > 5:
            result['long_func_num'] = PdfFeatureExtractor.MULTI
        elif ObjFeature.long_func_num > 1:
            result['long_func_num'] = PdfFeatureExtractor.FEW
        else:
            result['long_func_num'] = ObjFeature.long_func_num
        # 含有长字符串
        # result['has_long_str'] = 1 if ObjFeature.has_long_str else 0
        # 长字符串数量
        if ObjFeature.long_str_num > 5:
            result['long_str_num'] = PdfFeatureExtractor.MULTI
        elif ObjFeature.long_str_num > 1:
            result['long_str_num'] = PdfFeatureExtractor.FEW
        else:
            result['long_str_num'] = ObjFeature.long_str_num
        # 有混淆过的字符串
        # result['has_confused_str'] = 1 if ObjFeature.has_confused_str else 0
        # 混淆过的字符串的数量
        if ObjFeature.confused_str_num > 5:
            result['confused_str_num'] = PdfFeatureExtractor.MULTI
        elif ObjFeature.confused_str_num > 1:
            result['confused_str_num'] = PdfFeatureExtractor.FEW
        else:
            result['confused_str_num'] = ObjFeature.confused_str_num
        # 混淆过的字符串的总长度
        if ObjFeature.confused_str_length > 50:
            result['confused_str_length'] = PdfFeatureExtractor.LONG
        elif ObjFeature.confused_str_length >= 1:
            result['confused_str_length'] = PdfFeatureExtractor.SHORT
        else:
            result['confused_str_length'] = ObjFeature.confused_str_length
        # 含有多个'+'的字符串数量
        if ObjFeature.multi_plus_str > 5:
            result['multi_plus_str'] = PdfFeatureExtractor.MULTI
        elif ObjFeature.multi_plus_str > 1:
            result['multi_plus_str'] = PdfFeatureExtractor.FEW
        else:
            result['multi_plus_str'] = ObjFeature.multi_plus_str
        # （保留）是否含有Annot关键字
        result['has_Annot'] = 1 if ObjFeature.has_Annot else 0
        # 记录函数名出现在长字符串中func:num
        if ObjFeature.funcs_in_str:
            result['funcs_in_str'] = 1
        # suspicious_api
        for key in ObjFeature.suspicious_api.keys():
            if ObjFeature.suspicious_api[key] > 5:
                suspicious_api[key] = PdfFeatureExtractor.MULTI
            elif ObjFeature.suspicious_api[key] > 1:
                suspicious_api[key] = PdfFeatureExtractor.FEW
            else:
                suspicious_api[key] = ObjFeature.suspicious_api[key]
        # END #
        return result

    
    def get_js_records(self, js_result):
        data = []
        keys = sorted(js_result.keys())
        for key in keys:
            if key == 'suspicious_api':
                suspicious_api = js_result['suspicious_api']
                api_keys = sorted(suspicious_api.keys())
                for api_key in api_keys:
                    data.append(str(suspicious_api[api_key]))
            else:
                data.append(str(js_result[key]))
        return data

        
#++++++++++++++++ APIs +++++++++++++++++++

def get_pdf_features(data, filename):
    pdf = PdfFeatureExtractor(data, filename)
    pdf.extract_features()
    # 归一化
    def normalize(dict):
        """
        输入待归一的dict，返回归一后的dict
        """
        import copy
        result = copy.copy(dict)
        for key in result.keys():
            if result[key] > 0:
                result[key] = 1
        return result
        
    Leaf = normalize(pdf.LEAF)
    Node = normalize(pdf.NODE)
    OpenAction = normalize(pdf.OPENACTION)
    Outlines = normalize(pdf.OUTLINES)
    Page = normalize(pdf.PAGE)
    Pages = normalize(pdf.PAGES)
    Root = normalize(pdf.ROOT)
    Trailer = normalize(pdf.TRAILER)
    JS = pdf.JS
    
    # 向量合并
    def trans_dict_to_list(dict):
        """
        按key的字符顺序转化
        """
        data = []
        keys = sorted(dict.keys())
        for key in keys:
            data.append(str(dict[key]))
        return data
    
    list = []
    list = trans_dict_to_list(Leaf)
    list.extend(trans_dict_to_list(Node))
    list.extend(trans_dict_to_list(OpenAction))
    list.extend(trans_dict_to_list(Outlines))
    list.extend(trans_dict_to_list(Page))
    list.extend(trans_dict_to_list(Pages))
    list.extend(trans_dict_to_list(Root))
    list.extend(trans_dict_to_list(Trailer))
    list.extend(pdf.get_js_records(JS))
    return list
    
def record_features_to_file(records, file):
    """
    将向量记录到文件中
    """
    with open(file, 'a') as fw:
        fw.write(','.join(records))
        fw.write('\n')
    
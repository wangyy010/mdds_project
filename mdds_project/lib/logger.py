#!/usr/bin/env python 2.7
# -*- coding: utf-8 -*-

import logging

def set_logger(prog_name, log_path):
    logger = logging.getLogger(prog_name)
    logger.setLevel(logging.DEBUG)
    
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - \
        %(doudule)s.%(funcName)s.%(lineno)d - \
        %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    
    return logger
#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import env
import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning
build_exe_options = {'packages':['os', 'numpy', 'sklearn'], 'excludes':[]}

setup(name = 'multi_thread_detect.exe',
      version = '1.0',
      description = 'none',
      options = {'build_exe': build_exe_options},
      executables = [Executable('multi_thread_detect.py')]
      )
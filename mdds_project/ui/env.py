#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# append module's root directory to sys.path
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                    os.path.abspath(__file__)
                )
    )
    )
)
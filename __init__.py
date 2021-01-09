#!/usr/bin/env python
# encoding: utf-8

import sys
from os.path import abspath, join, dirname
print(join(abspath(dirname(__file__))))
sys.path.insert(0, join(abspath(dirname(__file__))))
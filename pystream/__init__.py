#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import ConfigParser
import os
import sys

__author__ = 'Libby Hemphill'
__email__ = 'libbyh@gmail.com'
__version__ = '0.1.1'

config = ConfigParser.RawConfigParser()

if 'PYSTREAM_CFG' in os.environ:
    config.read(os.environ['PYSTREAM_CFG'])
else:
    config.read('~/.pystream')
    
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

# make directories for storing data
path = config.get('data', 'path')
for subdir in 'jsons':
    try:
        os.makedirs(path + '/' + config.get('data', subdir))
    except:
        pass
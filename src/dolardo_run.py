#!/usr/bin/python
#encoding: utf-8
'''
Created on Aug 15, 2009

@author: santiago
'''

import os
import sys

current_path = os.getcwd()
sys.path.append(current_path)
sys.path.insert(0, '/home/santiag0/.python-eggs/MySQL_python-1.2.3c1-py2.4-linux-i686.egg')
os.chdir(os.path.join(current_path, "dolardo"))

from dolardo import dolardo_leer, dolardo_graficar, error_reporting

if __name__ == '__main__':
    dolardo_leer.leer_cotizaciones()
    #error_reporting.report("holaaaaa")

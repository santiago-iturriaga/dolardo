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
os.chdir(os.path.join(current_path, "dolardo"))

from dolardo import dolardo_leer, dolardo_graficar, error_reporting

if __name__ == '__main__':
    #dolardo_leer.leer_cotizaciones()
    error_reporting.report("holaaaaa")

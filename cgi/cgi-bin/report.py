#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 19:03:42 2017

@author: yiyuezhuo
"""

print("Content-type: text/html")
print("")

import subprocess
import os

def before(path):
    return os.path.split(path)[0]

master_root = before(before(before(__file__)))
#master_root = os.path.split(os.getcwd())[0]
#command = 'python CLI.py -re'
#os.environ['PATH'] += os.pathsep + master_root
config_path = os.path.join(master_root, 'config.json')
command = 'python ' + os.path.join(master_root, 'CLI.py') + ' -re -p ' + config_path
'''
try:
    result = subprocess.check_output(command, shell=True, env = os.environ)
except subprocess.CalledProcessError as e:
    #print('BUG')
    #print(os.environ)
    result = e.output
'''
os.chdir(master_root)
result = subprocess.check_output(command, shell=True)
#result = 'fake result'
print('<html><body>')
print('<h1>report</h1>')
print('<br>')
#print(command)
#print('<br>')
print(result.decode().replace('\n','<br>'))
print('</body></html>')

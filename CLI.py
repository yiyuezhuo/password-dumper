# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 12:11:33 2017

@author: yiyuezhuo
"""

import argparse
import json
from api import password_dump_six, report_cache

parser = argparse.ArgumentParser(description='Dump password')
parser.add_argument('-t', '--test', action='store_true')
parser.add_argument('-p', '--path', default='config.json')
parser.add_argument('-r', '--report', action='store_true')
parser.add_argument('-d', '--dump', action='store_true')
parser.add_argument('-q', '--quiet', action='store_true')
args = parser.parse_args()

if args.test:
    import pytesseract
    from PIL import Image
    
    im = Image.open('pic2.bmp')
    code = pytesseract.image_to_string(im)
    im.close()
    print('pytesseract test: result:{} expect:{}'.format(code,'2558'))
    exit()
    
with open(args.json) as f:
    config = json.load(f)
teacher_list = config['teacher_list']

verbose = not args.quiet

if args.report:
    report_cache(teacher_list)
if args.dump:
    password_dump_six(teacher_list, verbose = verbose)


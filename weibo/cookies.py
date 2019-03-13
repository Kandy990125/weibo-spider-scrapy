# encoding=utf-8
import json
import base64
import os

import requests
from selenium import webdriver
import time
from PIL import Image
from bs4 import BeautifulSoup
import re
import urllib

"""
输入你的账号和密码，可去淘宝买，一元七个。
建议买几十个，限制的严，太频繁了会出现302转移。
或者你也可以把时间间隔调大点。
"""
myAccount = [
    {'no': '13161276933', 'psw': 'yxj3466843'},
{'no': '13753520878', 'psw': 'sehunlimoran'},
]

headers={
    "Host":"login.weibo.cn",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Accept":'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept-Encoding":"gzip, deflate",
    "Connection":"keep-alive"
}
'''
# 获取验证码等相关登录信息
def get_captchainfo(loginURL):
    html = requests.get(loginURL).content
    bs = BeautifulSoup(html)
    #print bs
    #注意通过bs.select元素寻找对象，返回的是列表对象
    password_name = (bs.select('input[type="password"]'))[0].get('name')
    vk = (bs.select('input[name="vk"]'))[0].get('value')
    capId = (bs.select('input[name="capId"]'))[0].get('value')
    print password_name,vk,capId
    try:
        captcha_img = bs.find("img", src=re.compile('http://weibo.cn/interface/f/ttt/captcha/')).get('src')
        print captcha_img
        #captchaid可以从验证码图片地址中直接截取获得
        urllib.urlretrieve(captcha_img, 'captcha.jpg')
        print "captcha download success!"
        captcha_input = input("please input the captcha\n>")
    except:
        return None

    return (captcha_input,password_name,vk,capId)



def getCookies(weibo):
    """ 获取Cookies """
    cookies = []
    loginURL = 'http://login.weibo.cn/login/'
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        captcha = get_captchainfo(loginURL)
        if captcha[0] is None:
            #不需要验证码时的表单,微博网页版都要验证码，此处可以忽略
            postData = {
                    "source": "None",
                    "redir": "http://weibo.cn/",
                    "mobile": account,
                    "password": password,
                    "login": "登录",
            }
        else:
            #需要验证码时的表单
            print "提交表单数据"
            postData = {
                    "mobile": account,
                    captcha[1]: password,
                    "code": captcha[0],
                    "remember":"on",
                    "backurl": "http://weibo.cn/",
                    "backtitle":u'微博',
                    "tryCount":"",
                    "vk": captcha[2],
                    "capId": captcha[3],
                    "submit": u'登录',
            }
        print postData
        session = requests.Session()
        r = session.post(loginURL, data=postData, headers=headers)
        #判断post过后是否跳转页面
        #time.sleep(2)
        print r.url
        if r.url == 'http://weibo.cn/?PHPSESSID=&vt=1'or 'http://weibo.cn/?PHPSESSID=&vt=4':
            ceshihtml = requests.get(r.url).content
            print ceshihtml
            print 'Login successfully!!!'
            cookie = session.cookies.get_dict()
            cookies.append(cookie)
        else:
            print "login failed!"

    return cookies
'''

def getcookieByDriver(weibo):
    driver = webdriver.Chrome()
    driver.maximize_window()
    cookies = []
    for elem in weibo:
        account = elem['no']
        password = elem['psw']
        driver.get("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Flogin.weibo.cn%2Flogin%2F")
        time.sleep(3)
        elem_user = driver.find_element_by_xpath("//input[@id='loginName']")
        elem_user.send_keys(account)  # 用户名
        #微博的password有加后缀,
        elem_pwd = driver.find_element_by_xpath("//input[@id='loginPassword']")
        elem_pwd.send_keys(password)  # 密码
        time.sleep(3)
        #手动输验证码时间
        elem_sub = driver.find_element_by_xpath("//a[@id='loginAction']")
        elem_sub.click()  # 点击登陆
        time.sleep(2)
        weibo_cookies = driver.get_cookies()
        #cookie = [item["name"] + "=" + item["value"] for item in douban_cookies]
        #cookiestr = '; '.join(item for item in cookie)
        cookies.append(weibo_cookies)
    return cookies


#cookies = getCookies(myAccount)
cookies = getcookieByDriver(myAccount)
print("Get Cookies Finish!( Num:%d)" % len(cookies))



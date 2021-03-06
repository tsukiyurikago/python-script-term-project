#!/usr/bin/python
# coding=utf-8

import sys
import time
import sqlite3
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import date, datetime, timedelta
import traceback
import http.client
import urllib
from urllib import parse
from xml.etree import ElementTree

key = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade? '
TOKEN = '899442700:AAG9h3vssGqPKB2KKAF7FZq2zxUkZYAKQho'
MAX_MSG_LENGTH = 300
#baseurl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?ServiceKey='+key
baseurl = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcRHTrade?ServiceKey='+key
bot = telepot.Bot(TOKEN)

def myGetUrlData(keyword, pageNum):
    server = "openapi.naver.com"
    client_id = "ZuLj_9774MFbh52EAnsz"
    client_secret = "0fgHPxzAdQ"
    conn = http.client.HTTPSConnection(server)
    #    keyword = keyword.encode("utf-8")
    conn.request("GET", ("/v1/search/doc.xml?query={0}&display=1&start=" + str(pageNum)).format(keyword),
                 None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
    req = conn.getresponse()
    print(req.status, req.reason)
    if req.status != 200:
        return "찾는 페이지로부터 정보를 받아올 수 없다"
    cLen = req.getheader("Content-Length")
    data = req.read(int(cLen)).decode('utf-8')
    eTree = ElementTree.fromstring(data)
    result = ''

    result = keyword.decode("utf-8") + str(pageNum) + "번째 결과:\n"

    if eval(eTree.find("channel").find("total").text) > 0:
        channelElements = eTree.getiterator("channel")
        for things in channelElements:
            itemElements = things.getiterator("item")
            for item in itemElements:
                title = item.find("link").text
                title = title.replace('<b>', '')
                title = title.replace('</b>', '')
                title += "\n\n"
                result += title

    n = eval(eTree.find("channel").find("total").text)
    return result


def myGetData(keyword, pageNum = 1):
    server = "openapi.naver.com"
    client_id = "ZuLj_9774MFbh52EAnsz"
    client_secret = "0fgHPxzAdQ"
    conn = http.client.HTTPSConnection(server)
#    keyword = keyword.encode("utf-8")
    conn.request("GET", ("/v1/search/doc.xml?query={0}&display=10&start="+str(pageNum)).format(keyword),
                 None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
    req = conn.getresponse()
    print(req.status, req.reason)
    cLen = req.getheader("Content-Length")
    data = req.read(int(cLen)).decode('utf-8')
    eTree = ElementTree.fromstring(data)
    result = ''

    result = keyword.decode("utf-8") + "의 검색결과로 [" + eTree.find("channel").find("total").text + "]개의 학술지가 있어\n\n" + str(pageNum) + "페이지:\n"

    if eval(eTree.find("channel").find("total").text) > 0:
        channelElements = eTree.getiterator("channel")
        for things in channelElements:
            itemElements = things.getiterator("item")
            i = 0
            for item in itemElements:
                title = str(pageNum + i) + '\n'
                title += item.find("title").text
                title = title.replace('<b>', '')
                title = title.replace('</b>', '')
                title += "\n네이버링크: "
                title += item.find("link").text
                title += '\n\n'
                result += title
                i += 1

    n = eval(eTree.find("channel").find("total").text)
    return result, n

def myGetNthData(keyword, pageNum = 1):
    server = "openapi.naver.com"
    client_id = "ZuLj_9774MFbh52EAnsz"
    client_secret = "0fgHPxzAdQ"
    conn = http.client.HTTPSConnection(server)
#    keyword = keyword.encode("utf-8")
    conn.request("GET", ("/v1/search/doc.xml?query={0}&display=10&start="+str(int(pageNum)*10+1)).format(keyword),
                 None, {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret})
    req = conn.getresponse()
    print(req.status, req.reason)
    if req.status != 200:
        return "찾는 페이지로부터 정보를 받아올 수 없다"
    cLen = req.getheader("Content-Length")
    data = req.read(int(cLen)).decode('utf-8')
    eTree = ElementTree.fromstring(data)
    result = ''

    result = keyword.decode("utf-8") + '\n' + str(pageNum) + "페이지:\n"

    if eval(eTree.find("channel").find("total").text) > 0:
        channelElements = eTree.getiterator("channel")
        for things in channelElements:
            itemElements = things.getiterator("item")
            i = 1
            for item in itemElements:
                title = str(int(pageNum)*10+i) + '\n'
                title += item.find("title").text
                title = title.replace('<b>', '')
                title = title.replace('</b>', '')
                title += "\n네이버링크: "
                title += item.find("link").text
                title += '\n\n'
                result += title
                i += 1

    n = eval(eTree.find("channel").find("total").text)
    return result

def getData(loc_param, date_param):
    res_list = []
    url = baseurl+'&LAWD_CD='+loc_param+'&DEAL_YMD='+date_param
    #print(url)
    res_body = urlopen(url).read()
    #print(res_body)
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('item')
    for item in items:
        item = re.sub('<.*?>', '|', item.text)
        parsed = item.split('|')
        try:
            row = parsed[3]+'/'+parsed[6]+'/'+parsed[7]+', '+parsed[4]+' '+parsed[5]+', '+parsed[8]+'m², '+parsed[11]+'F, '+parsed[1].strip()+'만원\n'
        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list

def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)

def run(date_param, param='11710'):
    conn = sqlite3.connect('logs.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS logs( user TEXT, log TEXT, PRIMARY KEY(user, log) )')
    conn.commit()

    user_cursor = sqlite3.connect('users.db').cursor()
    user_cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    user_cursor.execute('SELECT * from users')

    for data in user_cursor.fetchall():
        user, param = data[0], data[1]
        print(user, date_param, param)
        res_list = getData( param, date_param )
        msg = ''
        for r in res_list:
            try:
                cursor.execute('INSERT INTO logs (user,log) VALUES ("%s", "%s")'%(user,r))
            except sqlite3.IntegrityError:
                # 이미 해당 데이터가 있다는 것을 의미합니다.
                pass
            else:
                print( str(datetime.now()).split('.')[0], r )
                if len(r+msg)+1>MAX_MSG_LENGTH:
                    sendMessage( user, msg )
                    msg = r+'\n'
                else:
                    msg += r+'\n'
        if msg:
            sendMessage( user, msg )
    conn.commit()

if __name__=='__main__':
    today = date.today()
    current_month = today.strftime('%Y%m')

    print( '[',today,']received token :', TOKEN )

    pprint( bot.getMe() )

    run(current_month)

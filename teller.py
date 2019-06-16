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

import noti

class userstat:
    def __init__(self,id,keyword, pageMax):
        self.id=id
        self.keyword=keyword
        self.pageMax = pageMax
        self.currentNum = 0

users = []


def replyUrlData(user, keyword, pageNum):
    msg = ''
    res = noti.myGetUrlData(keyword, pageNum)
    msg += res

    noti.sendMessage(user, msg)


def replyMyData(user, keyword, pageNum = 1):
    msg = ''
    #res = noti.myGetData(keyword)
    #msg += res

    if len(users) == 0:
        n = 0
        res, n = noti.myGetData(keyword.encode("utf-8"))
        msg += res
        users.append(userstat(user,keyword, n))
    else:
        for item in users:
            if item.id == user:
                res = noti.myGetNthData(keyword.encode("utf-8"), pageNum)
                msg += res
                noti.sendMessage(user, msg)
                return
        n = 0
        res, n = noti.myGetData(keyword.encode("utf-8"))
        msg += res
        users.append(userstat(user,keyword, n))

    noti.sendMessage(user, msg)

def replyAptData(date_param, user, loc_param='11710'):
    print(user, date_param, loc_param)
    res_list = noti.getData( loc_param, date_param )
    msg = ''
    for r in res_list:
        print( str(datetime.now()).split('.')[0], r )
        if len(r+msg)+1>noti.MAX_MSG_LENGTH:
            noti.sendMessage( user, msg )
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        noti.sendMessage( user, msg )
    else:
        noti.sendMessage( user, '%s 기간에 해당하는 데이터가 없습니다.'%date_param )

def save( user, loc_param ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    try:
        cursor.execute('INSERT INTO users(user, location) VALUES ("%s", "%s")' % (user, loc_param))
    except sqlite3.IntegrityError:
        noti.sendMessage( user, '이미 해당 정보가 저장되어 있습니다.' )
        return
    else:
        noti.sendMessage( user, '저장되었습니다.' )
        conn.commit()

def check( user ):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users( user TEXT, location TEXT, PRIMARY KEY(user, location) )')
    cursor.execute('SELECT * from users WHERE user="%s"' % user)
    for data in cursor.fetchall():
        row = 'id:' + str(data[0]) + ', location:' + data[1]
        noti.sendMessage( user, row )


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
        return

    text = msg['text']
    args = text.split(' ')

    for item in users:
        if item.id == chat_id:
            print("이미검색중인아이디")
            if text.startswith('완료') and len(args) > 0:
                noti.sendMessage(item.id, '이제 그만 검색할게\n\n검색 [찾을단어] 로 다시 검색할 수 있어')
                users.remove(item)
            elif text.startswith('페이지') and len(args) > 1:
                if 0<int(args[1])<item.pageMax+1:
                    item.currentNum=int(args[1])
                    replyMyData( chat_id, item.keyword, args[1] )
                else:
                    noti.sendMessage(item.id, '1에서 '+str(item.pageMax)+"사이 페이지만 찾을 수 있어")
            # elif text.startswith('네이버') and len(args) > 0:
            #     replyUrlData( chat_id, item.keyword, item.currentNum )
            else:
                noti.sendMessage(item.id, '너는 지금' + item.keyword + '를 검색 중이고 다음 명령어를 들어줄게\n\n\'완료\' - 현재 검색을 끝냄\n\n\'페이지 [숫자]\' - [숫자]번째 자료를 찾아본다')

            return

    if text.startswith('지역') and len(args)>1:
        print('try to 지역', args[1])
        replyAptData( '201705', chat_id, args[1] )
    elif text.startswith('저장')  and len(args)>1:
        print('try to 저장', args[1])
        save( chat_id, args[1] )
    elif text.startswith('거래')  and len(args)>1:
        print('try to 거래', args[1])
        replyAptData(args[1] , chat_id, args[2])
    elif text.startswith('확인'):
        print('try to 확인')
        check( chat_id )
    elif text.startswith('검색') and len(args)>1:
        print('try to 우리꺼', args[1])
        replyMyData( chat_id, args[1] )
    else:
        noti.sendMessage(chat_id, '모르는 명령어입니다.\n명령어 목록:\n검색 찾을단어')


today = date.today()
current_month = today.strftime('%Y%m')

print( '[',today,']received token :', noti.TOKEN )

bot = telepot.Bot(noti.TOKEN)
pprint( bot.getMe() )

bot.message_loop(handle)

print('Listening...')

while 1:
  time.sleep(10)
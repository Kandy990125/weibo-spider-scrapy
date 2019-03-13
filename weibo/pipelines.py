# -*- coding: utf-8 -*-
import sqlite3
from weibo.items import BlogItem
import time

class MySQLStorePipeline(object):
    def __init__(self):
        now_time = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        minute = str(int(int(time.strftime(time.strftime('%M', time.localtime(time.time())))) / 30) * 30)
        if len(minute) < 2:
            minute = "0" + minute
        recent_time = str(now_time[0:10]) + str(minute)
        self.sqlname = "weibo" + recent_time
        self.conn = sqlite3.connect('ycy.sqlite3')
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute('CREATE TABLE %s (blog_id varchar(100),usr_id varchar (100),user_name varchar(20),user_sex varchar(20),user_stay_place varchar(20),user_place varchar(20),user_birth varchar(30),user_star varchar(20),content varchar (1000),reposts_count varchar (1000),comments_count varchar(1000),attitudes_count varchar(1000))' % (self.sqlname))
        except:
            # self.cursor.execute("DROP TABLE IF EXISTS "+ (self.sqlname) )
            # self.cursor.execute(
            #    'CREATE TABLE %s (blog_id varchar(100),usr_id varchar (100),user_name varchar(20),user_sex varchar(20),user_stay_place varchar(20),user_place varchar(20),user_birth varchar(30), user_star varchar(20),content varchar (1000))' % (
            #        self.sqlname))
            pass

    def process_item(self, item, spider):
        #curTime = datetime.datetime.now()
        if isinstance(item, BlogItem):
            # try:
            # print("insert into %s (blog_id,usr_id,user_name,user_sex,user_stay_place,user_place,user_birth, user_star,content) values('%s','%s','%s','%s','%s','%s','%s','%s','%s')"
            #                         % (self.sqlname, str(item["Blog_ID"]),str(item["User_ID"]),str(item["User_name"]), str(item["User_sex"]),str(item["User_place"]),str(item["User_home"]),str(item["User_birth"]),str(item["User_star"]),str(item["Blog_content"])))
            self.cursor.execute("insert into %s (blog_id,usr_id,user_name,user_sex,user_stay_place,user_place,user_birth, user_star,content,reposts_count,comments_count,attitudes_count) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
                                    % (self.sqlname, str(item["Blog_ID"]),str(item["User_ID"]),str(item["User_name"]), str(item["User_sex"]),str(item["User_place"]),str(item["User_home"]),str(item["User_birth"]),str(item["User_star"]),str(item["Blog_content"]),str(item["reposts_count"]),str(item["comments_count"]),str(item["attitudes_count"])))
            self.conn.commit()

        return item

# coding=utf-8
from scrapy.spider import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from weibo.items import BlogItem
import re
import requests
from bs4 import BeautifulSoup
import json

class Weibo(Spider):
    name = "weibospider"
    allowed_domains=["m.weibo.cn"]
    start_urls=[]
    Blog_ID_list = []
    for i in range(3,105):
        # start_urls.append(
    #             "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E9%93%81%E8%B7%AF&page_type=searchall&page=" + str(
    #                 i))  # 铁路
    #         start_urls.append(
    #             "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E9%AB%98%E9%93%81&page_type=searchall&page=" + str(
    #                 i))  # 高铁
    #         start_urls.append(
    #             "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E9%93%81%E8%B7%AF&page_type=searchall&page=" + str(
    #                 i))  # 铁道
    #         start_urls.append(
    #             "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D%E4%BA%A4%E9%80%9A&page_type=searchall&page=" + str(
    #                 i))  # 交通
        start_urls.append(
            "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D%E6%9D%A8%E8%B6%85%E8%B6%8A%26t%3D0&page_type=searchall&page=" + str(
                i))

    def parse(self,response):
        text=response.body
        text=json.loads(text)
        data_group=text["data"]["cards"][0]["card_group"]
        for data in data_group:
            item = BlogItem()
            Blog_ID = data["mblog"]["id"]
            User_ID = data["mblog"]["user"]["id"]
            item["reposts_count"] = data["mblog"]["reposts_count"]
            item["comments_count"] = data["mblog"]["comments_count"]
            item["attitudes_count"] = data["mblog"]["attitudes_count"]
            if Blog_ID in self.Blog_ID_list:
                continue
            self.Blog_ID_list.append(Blog_ID)
            # print(Blog_ID,User_ID)
            item["User_name"] = data["mblog"]["user"]["screen_name"]
            self.Blog_ID_list.append(str(Blog_ID))
            try:
                content = data["mblog"]["longText"]["longTextContent"]
            except:
                temp = data["mblog"]["text"]
                dr = re.compile(r'<[^>]+>', re.S)
                content = dr.sub(r"", temp)
                ''''except:
                    try:
                        content = data["mblog"]["raw_text"]
                    except:
                        continue'''''
            item["Blog_content"] = content
            item["Blog_ID"] = Blog_ID
            item["User_ID"] = User_ID
            User_url = "https://m.weibo.cn/api/container/getIndex?containerid=230283"+str(User_ID)+"_-_INFO&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=230283"+str(User_ID)
            yield Request(url=User_url, meta={"item": item, "ID": User_ID, "Blog_ID":Blog_ID,"URL": User_url},
                              callback=self.parse1)

    def parse1(self,response):
        myitem = response.meta["item"]
        myitem['User_ID'] = response.meta["ID"]
        text = response.body
        text = json.loads(text)
        info_card = text["data"]["cards"][1]["card_group"]
        array = []
        sex = ""
        stay_place = ""
        home = ""
        birth = ""
        star = ""
        for item in info_card:
            #                                 print(item)
            if item["card_type"] == 42:
                continue
            dir = {}
            dir["item_name"] = item["item_name"]
            dir["item_content"] = item["item_content"]
            array.append(dir)
        for item in array:
            if item["item_name"] == "性别":
                sex = item["item_content"]
                continue
            if item["item_name"] == "所在地":
                stay_place = item["item_content"]
                continue
            if item["item_name"] == "家乡":
                home = item["item_content"]
                continue
            if item["item_name"] == "生日":
                birth = str(item["item_content"]).split(' ')[0]
                try:
                    star = str(item["item_content"]).split(' ')[1]
                    continue
                except:
                    continue
        myitem["User_place"] = stay_place
        myitem["User_home"] = home
        myitem["User_sex"] = sex
        myitem["User_birth"] = birth
        myitem["User_star"] = star
        yield  myitem
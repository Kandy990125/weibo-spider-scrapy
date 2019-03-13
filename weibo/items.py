# encoding=utf-8

from scrapy.item import Item, Field

class BlogItem(Item):
    Blog_ID = Field()  # 微博ID
    Blog_content = Field() # 微博内容
    User_ID = Field() # 用户ID
    User_name = Field()  # 用户名
    User_place = Field()  # 用户所在地
    User_home = Field()  # 用户家乡
    User_sex = Field()  # 用户性别
    User_birth = Field()
    User_star = Field()
    reposts_count = Field()
    comments_count = Field()
    attitudes_count = Field()
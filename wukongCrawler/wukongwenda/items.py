# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WukongwendaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ''' question info'''
    ques_id = scrapy.Field()
    ques_title = scrapy.Field()
    ques_status = scrapy.Field()
    ques_show_time = scrapy.Field()
    ques_follow_count = scrapy.Field()
    ques_nice_ans_count = scrapy.Field()
    ques_content = scrapy.Field()
    ques_create_time = scrapy.Field()
    ques_user_info = scrapy.Field()

    ''' detail info'''
    detail_ansid = scrapy.Field()
    detail_title = scrapy.Field()
    detail_status = scrapy.Field()
    detail_show_time = scrapy.Field()
    detail_content_abstract = scrapy.Field()
    detail_digg_count = scrapy.Field()
    detail_content = scrapy.Field()
    detail_brow_count = scrapy.Field()
    detail_comment_count = scrapy.Field()
    detail_create_time = scrapy.Field()
    detail_user_info = scrapy.Field()

    crawler_time = scrapy.Field()
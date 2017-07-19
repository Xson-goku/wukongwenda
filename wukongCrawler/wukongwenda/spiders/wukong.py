# -*- coding: utf-8 -*-

import scrapy
import os
import sys
import time
from datetime import datetime
import random
import json
import logging
import redis
from wukongwenda import settings
from wukongwenda.items import WukongwendaItem

reload(sys)
sys.setdefaultencoding("utf-8")


class WukongSpider(scrapy.Spider):
    name = "wukong"
    allowed_domains = ["wukong.com"]
    start_urls = ['https://www.wukong.com']
    
    def start_requests(self):
        # redis_connection = redis.StrictRedis(
        #                         host = settings.get('REDIS_HOST'),
        #                         port = settings.get('REDIS_PORT'),
        #                         db = settings.get('REDIS_DB'),
        #                         password = settings.get('REDIS_PASSWORD')
        #                     )
        
        with open("/root/wukongCrawler/brand.txt", 'r') as f:
            for key_word in f.readlines():
                yield scrapy.Request(
                    'https://www.wukong.com/wenda/web/search/loadmore/?search_text={}&offset=0'.format(key_word),
                    method='GET',
                    callback=self.parse,
                    meta={'key_word': key_word},
                    headers={'Accept-Encoding': 'gzip, deflate, sdch'},
                    )
    
    def parse(self, response):
        '''crawler qid infomation '''
        
        key_word = response.meta['key_word']
        items = WukongwendaItem()
        try:
            root = response.body.decode("utf-8")
            json_response = json.loads(root)
        except Exception as e:
            logging.debug("json_response is wrong:{}".format(e))
            json_response = {}
        
        has_more = json_response.get('data').get('has_more', False)
        
        if has_more:
            offset = int(response.url.split('&offset=')[1]) + 15
            next_url = response.url.split('&offset=')[0] + '&offset=' + str(offset)
            
            yield scrapy.Request(next_url,
                                 method='GET',
                                 headers={
                                     'Accept-Encoding': 'gzip, deflate, sdch',
                                     'referer': 'https://www.wukong.com/search/?keyword={}'.format(key_word)
                                 },
                                 meta={'key_word': key_word},
                                 callback=self.parse
                                 )
            
            try:
                questions = json_response.get('data').get('feed_question')
            except Exception as e:
                logging.info("this url is finish:{0}{1}".format(response.url, e))
                return
            
            for ques in questions:
                item = {}
                try:
                    item['brand'] = key_word
                    question_info = ques.get('question')
                    item['ques_id'] = int(question_info.get('qid', 0))
                    qid = item.get("ques_id")
                    item['ques_title'] = question_info.get('title')
                    # title = ques.get('title')
                    item['ques_status'] = question_info.get('status', 0)
                    item['ques_show_time'] = question_info.get('show_time')
                    item['ques_follow_count'] = question_info.get('follow_count', 0)
                    item['ques_nice_ans_count'] = question_info.get('nice_ans_count', 0)
                    item['ques_content'] = question_info.get('content').get('text')
                    item['ques_create_time'] = question_info.get('create_time', 0)
                    item['ques_user_info'] = question_info.get('user')
                    yield scrapy.Request(
                        'https://www.wukong.com/wenda/web/question/loadmorev1/?qid={}&count=10&req_type=2&offset=0'.format(
                            qid),
                        method='GET',
                        headers={'Accept-Encoding': 'gzip, deflate, sdch'},
                        meta={
                            'item': item,
                            'qid': qid
                        },
                        callback=self.parse_detail
                        )

                except Exception as e:
                    logging.debug('item is wrong:{}'.format(e))
        else:
            try:
                questions = json_response.get('data').get('feed_question')
            except Exception as e:
                logging.info("this url is finish:{0}{1}".format(response.url, e))
                return
            
            for ques in questions:
                item = {}
                try:
                    item['brand'] = key_word
                    question_info = ques.get('question')
                    item['ques_id'] = int(question_info.get('qid', 0))
                    qid = item.get("ques_id")
                    item['ques_title'] = question_info.get('title')
                    # title = ques.get('title')
                    item['ques_tatus'] = question_info.get('status', 0)
                    item['ques_show_time'] = question_info.get('show_time')
                    item['ques_follow_count'] = question_info.get('follow_count', 0)
                    item['ques_nice_ans_count'] = question_info.get('nice_ans_count', 0)
                    item['ques_content'] = question_info.get('content').get('text')
                    item['ques_create_time'] = question_info.get('create_time', 0)
                    item['ques_user_info'] = question_info.get('user')
                    yield scrapy.Request(
                        'https://www.wukong.com/wenda/web/question/loadmorev1/?qid={}&count=10&req_type=2&offset=0'.format(
                            qid),
                        method='GET',
                        headers={'Accept-Encoding': 'gzip, deflate, sdch'},
                        meta={
                            'item': item,
                            'qid': qid
                        },
                        callback=self.parse_detail
                        )
                except Exception as e:
                    logging.debug('item is wrong:{}'.format(e))
    
    def parse_detail(self, response):
        """crawler detail infomation"""
        item = response.meta['item']
        qid = response.meta['qid']
        
        try:
            root = response.body.decode("utf-8")
            json_response = json.loads(root)
        except Exception as e:
            logging.debug("json_response is wrong:{}".format(e))
            json_response = {}
        
        has_more = int(json_response.get('data').get('has_more', '0'))
        
        if has_more == 1:
            offset = int(response.url.split('&offset=')[1]) + 10
            next_url = response.url.split('&offset=')[0] + '&offset=' + str(offset)
            yield scrapy.Request(next_url,
                                 headers={'Accept-Encoding': 'gzip, deflate, sdch',
                                          'rederer': 'https://www.wukong.com/question/{}/'.format(qid)},
                                 method='GET',
                                 meta={'item': item, 'qid': qid},
                                 callback=self.parse_detail,
                )
            
            try:
                ans_list = json_response.get('data').get("ans_list")
            except Exception as e:
                logging.info("this url is finish:{0}{1}".format(response.url, e))
                return
            
            for ans in ans_list:
                try:
                    item['_id'] = int(ans.get('ansid', 0))
                    ansid = item.get("_id")
                    item['detail_title'] = ans.get('title')
                    # title = ques.get('title')
                    item['detail_status'] = ans.get('status', 0)
                    item['detail_show_time'] = ans.get('show_time')
                    item['detail_content_abstract'] = ans.get('content_abstract', 0)
                    item['detail_digg_count'] = ans.get('digg_count', 0)
                    item['detail_content'] = ans.get('content').replace('<p>', '').replace('</p>', '')
                    item['detail_brow_count'] = ans.get('brow_count')
                    item['detail_comment_count'] = ans.get('comment_count')
                    item['detail_create_time'] = ans.get('create_time', 0)
                    item['detail_user_info'] = ans.get('user')
                    item['crawler_time'] = str(datetime.now())[:19]
                    
                    yield item
                except Exception as e:
                    logging.debug('item is wrong:{}'.format(e))
        
        else:
            try:
                ans_list = json_response.get('data').get("ans_list")
            except Exception as e:
                logging.info("this url is finish:{0}{1}".format(response.url, e))
                return
            
            for ans in ans_list:
                try:
                    item['_id'] = int(ans.get('ansid', 0))
                    ansid = item.get("_id")
                    item['detail_title'] = ans.get('title')
                    # title = ques.get('title')
                    item['detail_status'] = ans.get('status', 0)
                    item['detail_show_time'] = ans.get('show_time')
                    item['detail_content_abstract'] = ans.get('content_abstract', 0)
                    item['detail_digg_count'] = ans.get('digg_count', 0)
                    item['detail_content'] = ans.get('content').replace('<p>', '').replace('</p>', '')
                    item['detail_brow_count'] = ans.get('brow_count')
                    item['detail_comment_count'] = ans.get('comment_count')
                    item['detail_create_time'] = ans.get('create_time', 0)
                    item['detail_user_info'] = ans.get('user')
                    item['crawler_time'] = str(datetime.now())[:19]
                    
                    yield item
                
                except Exception as e:
                    logging.debug('item is wrong:{}'.format(e))

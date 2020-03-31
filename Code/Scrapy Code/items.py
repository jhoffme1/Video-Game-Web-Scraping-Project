# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class VideogamesItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    genre = scrapy.Field()
    developer = scrapy.Field()
    release_date = scrapy.Field()
    seperate_reviews = scrapy.Field()
    user_score = scrapy.Field()
    review_critic= scrapy.Field()
    review_grade = scrapy.Field()
    # review_date = scrapy.Field()
    # review= scrapy.Field()
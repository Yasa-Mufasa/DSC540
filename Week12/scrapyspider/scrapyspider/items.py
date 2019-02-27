# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EmojiSpiderItem(scrapy.Item):
    emoji_handle = scrapy.Field()
    emoji_image = scrapy.Field()
    section = scrapy.Field()
    emoji_link = scrapy.Field() # Adding this field addresses the error I was receiving about the emoji_link not existing. It also grabs more data from teh website.

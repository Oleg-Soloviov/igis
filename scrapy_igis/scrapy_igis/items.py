# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyIgisItem(scrapy.Item):
    site_address = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    x_coord = scrapy.Field()
    y_coord = scrapy.Field()
    hospital_address = scrapy.Field()
    hospital_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()
    place_url = scrapy.Field()


class ScrapyIgisIzhItem(scrapy.Item):
    site_address = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    x_coord = scrapy.Field()
    y_coord = scrapy.Field()
    hospital_address = scrapy.Field()
    hospital_name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    url = scrapy.Field()
    slug = scrapy.Field()


class PersonIgisItem(scrapy.Item):
    fio = scrapy.Field()
    update_date = scrapy.Field()
    speciality = scrapy.Field()
    room = scrapy.Field()
    time_limit = scrapy.Field()
    kod = scrapy.Field()
    sector = scrapy.Field()
    time_filter = scrapy.Field()
    unit = scrapy.Field()
    info = scrapy.Field()
    igis_url = scrapy.Field()
    igis_obj = scrapy.Field()
    igis_person_id = scrapy.Field()
    free_days = scrapy.Field()
    not_working_days = scrapy.Field()

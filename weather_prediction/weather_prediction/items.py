# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class WeatherPredictionItem(Item):
    time = Field()
    temperature = Field()
    pressure = Field()
    wind = Field()
    humidity = Field()
    day = Field()

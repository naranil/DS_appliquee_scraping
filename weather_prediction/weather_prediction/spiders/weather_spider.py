# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from weather_prediction.items import WeatherPredictionItem

class WeatherSpider(BaseSpider):
   name = "weather"
   allowed_domains = ["meteociel.fr"]
   start_urls = [
       "http://www.meteociel.fr/tendances/25627/lyon.htm"
   ]

   def parse(self, response):
       #sel = Selector(response)
       #sites = response.xpath('//center/table/tr/td/table/tr/td')
       items = []
       #for site in sites:
       #    item = WeatherPredictionItem()
       #    item['time'] = site.xpath('text()').re('\d\d:\d\d')
       #    item['temperature'] = site.xpath('text()').re('.* \xb0C$')
       #    item['pressure'] = site.xpath('text()').re('.* hPa$')
       #    item['wind'] = site.xpath('img/@title').re('.* : .*')
       #    item['humidity'] = site.xpath('text()').re('.* %$')

       #    items.append(item)
       #return items
       # Extract the time
       print response.xpath('//center/table/tr/td/table/tr/td/text()').re('\d\d:\d\d')
      # Extract the temperature
       print response.xpath('//center/table/tr/td/table/tr/td/text()').re('.* \xb0C$')

      # Extract the pression
       print response.xpath('//center/table/tr/td/table/tr/td/text()').re('.* hPa$')
      # Direction vent
       print response.xpath('//center/table/tr/td/table/tr/td/img/@title').re('.* : .*')
      # Humidité
       print response.xpath('//center/table/tr/td/table/tr/td/text()').re('.* %$')
      # Temps
       print response.xpath('//center/table/tr/td/table/tr/td/img/@title').extract()
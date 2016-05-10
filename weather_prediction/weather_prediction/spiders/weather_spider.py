import datetime
import calendar

from scrapy.spider import BaseSpider
from scrapy.selector import Selector

from weather_prediction.items import WeatherPredictionItem

import pandas as pd
import os

class WeatherSpider(BaseSpider):
   name = "weather"
   allowed_domains = ["meteociel.fr"]
   start_urls = [
       "http://www.meteociel.fr/previsions/25627/lyon.htm"
   ]

   def parse(self, response):
       now = datetime.datetime.now()
       month = now.month
       year = now.year
       tr_selectors = response.xpath("//center/table/tr/td/table/tr")
       output = {}
       data = pd.DataFrame(columns=["temperature",
                                    "wind_direction",
                                    "wind_speed",
                                    "gust",
                                    "rain",
                                    "humidity",
                                    "pressure",
                                    "weather"])

       for tr_selector in tr_selectors:
        if len(tr_selector.xpath("./td")) > 8:
          if len(tr_selector.xpath("./td")) == 10:       
            i = 1
            print ""
            # Extract day time
            day = tr_selector.xpath("./td")[0].xpath("./text()").extract()
            print "Jour ", day[0], " ", day[1]
            day_num = day[1]
            day = day[0] + " " + day[1]

            output[day] = {}

          else:
            i = 0

          # Extract time: Date format -> hh:mm dd/mm/yyyy
          time = tr_selector.xpath("./td")[i].xpath("./text()").extract()
          print "Heure ", time[0]
          output[day]["time"] = time[0]
          complete_day = time[0] + ' ' + str(day_num) + '/' + '0' + str(month) + '/' + str(year) \
                          if len(str(month)) == 1 \
                          else \
                            time[0] + ' ' + str(day_num) + '/' + str(month) + '/' + str(year)

          # For month and year changing
          if day_num == 31 and month < 12:
            month += 1
          if day_num == 31 and month == 12:
            month = 1
            year += 1
          if day_num == 30 and month in [4, 6, 9, 11]:
            month += 1
          if calendar.isleap(year):
            if day_num == 29 and month == 2:
              month += 1
          else:
            if day_num == 28 and month == 2:
              month += 1

          # Extract the temperature
          temperature = tr_selector.xpath("./td")[i+1].xpath("./text()").extract()
          print "Temperature ", temperature[0]
          output[day]["temperature"] = temperature[0]
          data.ix[complete_day, "temperature"] = temperature[0]

          # Wind direction
          wind_direction = tr_selector.xpath("./td")[i+2].xpath("./img/@title").extract()
          print "Wind direction ", wind_direction[0]
          output[day]["wind_direction"] = wind_direction[0]
          data.ix[complete_day, "wind_direction"] = wind_direction[0]

          # Wind speed
          wind_speed = tr_selector.xpath("./td")[i+3].xpath("./text()").extract() 
          print "Wind speed ", wind_speed[0]
          output[day]["wind_speed"] = wind_speed[0]
          data.ix[complete_day, "wind_speed"] = wind_speed[0]

          # Gust
          gust = tr_selector.xpath("./td")[i+4].xpath("./text()").extract()
          print "Gust ", gust[0]
          output[day]["gust"] = gust[0]
          data.ix[complete_day, "gust"] = gust[0]

          # Rain
          rain = tr_selector.xpath("./td")[i+5].xpath(".//text()").extract()
          print "Rain ", rain[0]
          output[day]["rain"] = rain[0]
          data.ix[complete_day, "rain"] = rain[0]

          # Humidity
          humidity = tr_selector.xpath("./td")[i+6].xpath("./text()").extract()
          print "Humidity ", humidity[0]
          output[day]["humidity"] = humidity[0]
          data.ix[complete_day, "humidity"] = humidity[0]

          # Pressure
          pressure = tr_selector.xpath("./td")[i+7].xpath("./text()").extract()
          print "Pressure ", pressure[0] 
          output[day]["pressure"] = pressure[0] 
          data.ix[complete_day, "pressure"] = pressure[0]      

          # Weather
          weather = tr_selector.xpath("./td")[i+8].xpath("./img/@title").extract()
          print "Weather ", weather[0] 
          output[day]["weather"] = weather[0]  
          data.ix[complete_day, "weather"] = weather[0]           

          print ""    

       # Save the results in CSV format
       data.to_csv('./output/result.csv', encoding='utf-8', index_label="time")
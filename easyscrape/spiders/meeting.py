import scrapy
import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime
from dateutil.parser import parse
from urllib.parse import urlparse




from scrapy import Spider
from scrapy.http import FormRequest,Request
from scrapy.utils.response import open_in_browser
 

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class MeetingSpider(scrapy.Spider):
    name = 'meetings'
    start_urls = ['https://toastmasterclub.org/login.php']
    member_ids = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'easyscrape.pipelines.MeetingPipeline': 300,
        }
    }


    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'cwlv', 'password': '9752f82d'},
            callback=self.after_login
        )

    def after_login(self, response):
        url = 'https://toastmasterclub.org/view_meeting.php?c=486&show=next'
        yield Request(
                url=url,
                callback=self.action)


    def action(self, response):
        with open('tm_meetings.csv', 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "Name","Date"])
        
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        previous_link = soup.find(string="Previous").find_parent("a")
        href = previous_link['href']
        last_url = f'https://toastmasterclub.org/{href}'
        yield Request(url=last_url,callback=self.get_meeting_history)
            
        
            

    def get_meeting_history(self,response):
        
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        previous_link = soup.find(string="Previous").find_parent("a")
        if previous_link:
            href = previous_link['href']
            last_url = f'https://toastmasterclub.org/{href}'
            main_title = soup.find("td", {"class": "maintitle"})
            date_componenets = main_title.text.split(' ')
            meeting_datetime = parse(f'{date_componenets[1]} {date_componenets[2]} {date_componenets[3]} {date_componenets[5]}') 
            print(meeting_datetime)

            attendance_div = soup.find('div',{"id":"status_div_"})
            attendance_table = attendance_div.findChild()
            for tr in attendance_table.find_all('tr', recursive=False):
                name_span = tr.find('span',{"class":"nav"})
                if name_span:
                    name_anchor = name_span.findChild()
                    print(name_anchor.text)
                    p = re.compile(r'u=\d+')
                    p_match = p.search(name_anchor['onclick'])
                    if p_match:
                        user_id = p_match[0][2:]
                        print(user_id)


                


            yield Request(url=last_url,callback=self.get_meeting_history)
        else:
            print('doney done done')
        #yield item
        
        
            
       
   
       
       
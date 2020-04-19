import scrapy
import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime



from easyscrape.items import MemberItem

from scrapy import Spider
from scrapy.http import FormRequest,Request
from scrapy.utils.response import open_in_browser
 

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class MemberSpider(scrapy.Spider):
    name = 'member'
    start_urls = ['https://toastmasterclub.org/login.php']
    member_ids = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'easyscrape.pipelines.MemberPipeline': 300,
        }
    }

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'cwlv', 'password': '9752f82d'},
            callback=self.after_login
        )

    def after_login(self, response):
        url = 'https://toastmasterclub.org/memberchart.php?c=486&chart=9'
        yield Request(
                url=url,
                callback=self.action)


    def action(self, response):
        with open('tm_members.csv', 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "Name","Joined",])
        
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        workbook_history_table =  soup.find(string="Mentor").find_parent("table")
        l = []
        df = pd.read_html(str(workbook_history_table))
        table_rows = workbook_history_table.find_all('tr')
        users = []
     
        for tr in table_rows:
            
            td = tr.find_all('td')
            row = [i.text.strip('\n') for i in td]
            print(row)
            #if len(td) >3:
            if len(row) == 7:
                user_id = td[0].span.a['href'][-5:]
                row.append(user_id)
                users.append(row)    
                
            #    name = td[0].text.strip()
            #    joined = td[4].text.strip() 
            #    if [user_id,name,joined] not in users:
            #        users.append([user_id,name,joined])
            
        
        

        for row in users:
            with open('tm_members.csv', 'a', newline='\n', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(row)    
            
            join_date = datetime.strptime(row[4], '%d %b %y').date()

            member_data = {'full_name':row[0],'join_date':join_date,'es_id':row[7]}
            item = MemberItem(member_data)
            print('yuyuyu')

            
            yield item

           
            
    

    
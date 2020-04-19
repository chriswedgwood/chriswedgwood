import scrapy
import os
import pandas as pd
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime





from scrapy import Spider
from scrapy.http import FormRequest,Request
from scrapy.utils.response import open_in_browser
 

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    pass

class RoleSpider(scrapy.Spider):
    name = 'roles'
    start_urls = ['https://toastmasterclub.org/login.php']
    member_ids = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'easyscrape.pipelines.RolePipeline': 300,
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
        with open('tm_roles.csv', 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "Name","Role","Date"])
        
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        workbook_history_table =  soup.find(string="Mentor").find_parent("table")
        l = []
        df = pd.read_html(str(workbook_history_table))
        table_rows = workbook_history_table.find_all('tr')
        user_ids = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text.strip('\n') for i in td]
            print(row)
            if len(td) >1:
                user_id= td[0].span.a['href'][-5:]
                if user_id not in user_ids:
                    user_ids.append(user_id)
            
        print(f'USER_IDS:{user_ids}')

        for id in user_ids:
            url = f'https://toastmasterclub.org/tm_stats.php?u={id}&s=1'
            yield Request(url=url,callback=self.get_role_history,meta={'id':id})
            
        
            

    def get_role_history(self,response):
        
        id = response.meta.get('id')
      
        self.member_ids.append(id)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        name = soup.find('span',{"class": "maintitle"}).text
        roles_table = soup.find(string="Status").find_parent("table")
     
        table_rows = roles_table.find_all('tr')
        
        for tr in table_rows[1:]:
            
            role = None
            role_date = None    
            if tr.find('a'):
                role = tr.find('a').text
            if tr.find_all('span'):     
                role_date = tr.find_all('span')[-1].text.strip() 
                role_date = datetime.strptime(role_date, '%d %b %y').date()
            
            if role:
                item = {'es_id':id,'full_name':name,'role':role,'role_date':role_date} 
                yield item

        
        
            
       
   
       
       
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

class SpeechSpider(scrapy.Spider):
    name = 'speeches'
    start_urls = ['https://toastmasterclub.org/login.php']
    member_ids = []

    custom_settings = {
        'ITEM_PIPELINES': {
            'easyscrape.pipelines.SpeechPipeline': 300,
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
        with open('tm_speeches.csv', 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["id", "Name","Club","WorkBook","Speech","title","completed",""])
        
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
            #id = 20474
            url = f'https://toastmasterclub.org/profile_cc.php?u={id}'
            yield Request(url=url,callback=self.get_user_info,meta={'id':id})
            
        
            

    def get_user_info(self,response):
        pathways = []
        id = response.meta.get('id')
        print(f'id:{id}')
        self.member_ids.append(id)
        data = response.text
        soup = BeautifulSoup(data, features="lxml")
        workbook_history_table = soup.find(string="Workbook History").find_parent("table")
        workbooks_span = workbook_history_table.findAll("span", {"class": "smalltitle"}) 
        for index,tr in enumerate(workbook_history_table.find_all('tr', recursive=False)):
            td = tr.find_all('td')
            pathway = tr.find('span',{"class": "smalltitle"}) or None
            speech_span = tr.find('span',{"class": "gen"}) or None
            
            if pathway:
                pathway_text = pathway.text.strip().replace('(Pathway) ','')
                pathways.append(pathway_text)
            if speech_span:
                title = tr.find('a',{"class":"gen"})
                
                if speech_span.text:
                    assignment = speech_span.text.strip().replace('(Pathway) ','')
                
                if title:
                    
                    completed_obj = tr.findAll(text=re.compile('Completed '))
                    
                    if completed_obj:
                        completed_span = completed_obj[0].find_parent()
                        completed_a = completed_span.find_all('a')
                        
                        if len(completed_a)==1:
                            completed_date = completed_span.text[-9:]
                        else:
                            completed_date = completed_a[-1].text
                        
                        completed_date  = datetime.strptime(completed_date, '%d %b %y').date()
                        level = assignment[:7]
                        if level[:5]!='Level':
                            level = 'Level 1'
                        assignment = assignment[8:]
                        speech_data = {'pathway':pathways[-1],'level':level,'assignment':assignment,'speech_title':title.text,'completed_date':completed_date,'es_id':id}
                        yield speech_data
                        #print(f'Pathway:{pathways[-1]} assignment:{assignment} title:{title.text}completed:{completed_date}')

                
                
        
        # name_tr = soup.find(string="Name").find_parent("tr")
        # name_td = name_tr.find_all('td')[1]
        # name = name_td.text.strip()
        # date_joined_tr  = soup.find_all("span",text=re.compile("^Joined"))[0].find_parent("tr")
        # date_joined_td = date_joined_tr.find_all('span')[1]
        # date_joined = date_joined_td.text.strip()
        # data_row = [id,name,date_joined]

        # speeches_table = soup.find(string="All known speeches").find_parent("table")
        # table_rows = speeches_table.find_all('tr')
        # user_ids = []
        # for tr in table_rows:
        #     td = tr.find_all('td')
        #     row = [re.sub(' +', ' ',i.text.strip('\n').replace(u'\xa0', ' ').replace('completed ','')) for i in td] 
            
            
            
        #     print(row)
           
        #     if row and row[0] not in ['All known speeches','Requested and Scheduled Speeches'] :
        #         entire_row = ' '.join([str(col) for col in row])
        #         if 'Completed' in entire_row:
        #             row[4] = row[4].replace('Completed ','')
        #             row = [id,name] + row
        #             with open('tm_speeches.csv', 'a', newline='\n', encoding='utf-8') as f:
        #                 writer = csv.writer(f)
        #                 writer.writerow(row)

        
        
            
       
   
       
       
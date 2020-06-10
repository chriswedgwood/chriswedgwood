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
    attendance_history = []
    meeting_awards = []
    meeting_roles = []

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
        url = 'https://toastmasterclub.org/view_meeting.php?t=63903'
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
        previous = soup.find(string="Previous")
        if previous:
            previous_link = previous.find_parent("a")
            href = previous_link['href']
            last_url = f'https://toastmasterclub.org/{href}'
            main_title = soup.find("td", {"class": "maintitle"})
            date_componenets = main_title.text.split(' ')
            meeting_datetime = parse(f'{date_componenets[1]} {date_componenets[2]} {date_componenets[3]} {date_componenets[5]}') 
            
            #ATTENDANCE
            attendance_div = soup.find('div',{"id":"status_div_"})
            attendance_table = attendance_div.findChild()
            for tr in attendance_table.find_all('tr', recursive=False):
                name_span = tr.find('span',{"class":"nav"})
                if name_span:
                    name_anchor = name_span.findChild()
                    member_name = name_anchor.text
                    p = re.compile(r'u=\d+')
                    p_match = p.search(name_anchor['onclick'])
                    if p_match:
                        user_id = p_match[0][2:]
                       
                        self.attendance_history.append((meeting_datetime,member_name,user_id))
            #WINNERS
            ribbon = soup.findAll(text=re.compile("Ribbon /+"))
            if ribbon:
                ribbon_parent_tr = ribbon[0].findParent("tr")
                ribbon_tr_sibblings = ribbon_parent_tr.findNextSiblings()
                for tr in ribbon_tr_sibblings:
                    
                    tr_bold_html = tr.findAll('b')
                    if tr_bold_html:
                        award = tr_bold_html[0].text
                        name_anchor = tr_bold_html[1].findChild()
                        member_name = name_anchor.text
                        p = re.compile(r'u=\d+')
                        p_match = p.search(name_anchor['onclick'])
                        if p_match:  
                            user_id = p_match[0][2:]
                            
                            self.meeting_awards.append((meeting_datetime,award,member_name,user_id))
            #ACTUAL ROLES
            role_header = soup.findAll("th",{"class":"thLeft"},text='Role')
            if role_header:
                role_header_tr = role_header[0].findParent("tr")
                role_header_tr_sibblings = role_header_tr.findNextSiblings()
                for tr in role_header_tr_sibblings:
                    role_name_spans = tr.findAll('span')
                    if role_name_spans and len(role_name_spans) > 1:
                        role = role_name_spans[0].text.strip().replace(u'\xa0',' ')
                        
                        name_anchor = role_name_spans[1].findChild('a')
                        p = re.compile(r'u=\d+')
                        if name_anchor:
                            member_name = name_anchor.text
                            p_match = p.search(name_anchor['onclick'])
                        else:
                            member_name = role_name_spans[3].text.replace(u'\xa0',' ').strip()
                            name_anchor = role_name_spans[3].findChild('a')
                            if name_anchor:
                                p_match = p.search(name_anchor['onclick'])
                            
                        if p_match:  
                            user_id = p_match[0][2:]
                            self.meeting_roles.append((meeting_datetime,role,member_name,user_id)) 

            meeting_data = {'attendance':self.attendance_history,'awards':self.meeting_awards,'roles':self.meeting_roles}
            yield meeting_data
            yield Request(url=last_url,callback=self.get_meeting_history)
        else:
            #print(self.attendance_history)
            print(self.meeting_roles)
            meeting_data = {'attendance':self.attendance_history,'awards':self.meeting_awards,'roles':self.meeting_roles}
            yield meeting_data

        #yield item
        
        
            
       
   
       
       
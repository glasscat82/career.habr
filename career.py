import sys
import requests, fake_useragent  # pip install requests
import json
import re
from bs4 import BeautifulSoup

class career():
    """parsing for career.habr.com/experts"""
    def __init__(self, url="https://career.habr.com/experts?order=lastActive&page=1", filename="career.json"):
        self.url = url
        self.filename = filename

    @staticmethod
    def p(text, *args):
        print(text, *args, sep=' / ', end='\n')

    def write_json(self, data, path = None):
        path = self.filename if path is None else path
        with open(path, 'w', encoding='utf8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_json(self, path = None):
        path = self.filename if path is None else path
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
        return {}
    
    # Random User-Agent
    def get_html(self, url_page = None):
        ua = fake_useragent.UserAgent() 
        user = ua.random
        header = {'User-Agent':str(user)}
        url_page = self.url if url_page is None else url_page
        try:
            page = requests.get(url_page, headers = header, timeout = 10)
            return page.text
        except Exception as e:
            print(sys.exc_info()[1])
            return False
    
    def get_all_links(self, html):
        if html is False:
            return False

        soup = BeautifulSoup(html, 'lxml')
        selection_list = soup.find_all('div', class_='expert-card__main')        

        links = []
        for expert in selection_list:
            try:
                expert_header = expert.find('div', class_='expert-card__header')
                title_ = expert_header.find('h2', class_='expert-card__title')
                
                # time work user company and experience company
                experience = []
                for span_item in expert_header.find_all('span', class_='inline-list'):
                    item_ = [ex_.text.strip().replace('•', '').strip() for ex_ in span_item.find_all('span', recursive=False)]
                    experience.append(list(filter(None, item_)))

                # help sections block in servises user
                help_ = {}
                help_item = expert.find('div', {'class':'section-group section-group--gap-medium-large'})                               
                if help_item is not None:
                    hk = [hk0.text.strip() for hk0 in help_item.find_all('span', {'class':'basic-text basic-text--color-muted'})]
                    hv = [hk1.text.strip().replace('•', '|') for hk1 in help_item.find_all('span', {'class':'inline-list'})]

                    help_ = {x.replace(':', ''):hv[index] for index, x in enumerate(hk, 0)}

                # expert-cost
                cost_expert = {}
                cost_ = expert.find('div', {'class':'expert-cost'})                
                if cost_ is not None:
                    cost_expert = {f'prise_{index}':ce.text.strip() for index, ce in enumerate(cost_.find_all('div', recursive=False), 1)}
                
                # ava
                ava_user = None
                expert_card = expert.parent
                ava_user = expert_card.find('img', {'class':'basic-avatar__image'}).get('src')
                
                # time user auth
                basic_date = expert_card.find('time', {'class':'basic-date'}).get('datetime')

                row = {}
                row['title'] = title_.text.strip()
                row['slug'] = title_.find('a').get('href').replace('/', '')
                row['experience'] = experience
                row['helps'] = help_
                row['prise'] = cost_expert
                row['img'] = ava_user
                row['date'] = basic_date

                links.append(row)

            except Exception as e:
                print(sys.exc_info()[1])
                continue

        return links
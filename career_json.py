from urllib import request
import json
from fake_useragent import UserAgent

def get_data():
    url = 'https://career.habr.com/api/frontend_v1/experts?order=lastActive&page=1'    

    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-Agent': UserAgent().google,
    }

    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200:
        res = str(response.read(), encoding='utf8')
        # print(res)
        return res

def get_parse(html):
    # convert json in the form of strings
    data = json.loads(html)
    
    for exprt in data['list']:
        print(exprt['title'], exprt['login'])

if __name__ == '__main__':
	get_parse(get_data())
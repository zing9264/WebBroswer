import requests
import pandas as pd
import numpy as np
import hashlib
import csv
from bs4 import BeautifulSoup
import os
from functools import cmp_to_key

def parser(page):
    contextpool = []
    links = []

    '''
    opth = os.getcwd()
    path = opth+r'\htmldb\\'+idx+r".html"
    print(path)
    with open(path, 'r', encoding='UTF-8', newline='') as f:
        page=f.read()
    '''

    soup = BeautifulSoup(page, 'html.parser')
   # print(soup.prettify())
    title_tag = soup.title
    print(title_tag)
    
    # 所有的超連結
    a_tags = soup.find_all('a')
    for tag in a_tags:
        print(tag.string)
        # 輸出超連結
        links.append(str(tag.get('href')))
        # 輸出超連結的文字
        contextpool.append(str(tag.string).replace(' ','').replace(u'\u3000', '').replace(u'\xa0',''))

    div_tags = soup.find_all('div')
    for tag in div_tags:
    # 輸出DIV中的內文、並對其長度排序
        print(tag.string)
        contextpool.append(str(tag.string).replace(' ', '').replace(u'\u3000', '').replace(u'\xa0', ''))
        contextpool.sort(key=cmp_to_key(lambda x, y: len(y)-len(x)))
    contextpool = list(dict.fromkeys(contextpool))
    print(contextpool)
    print(links)

    return title_tag.string,contextpool,links


if __name__ == "__main__":
    pass

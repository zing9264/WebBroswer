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
    soup = BeautifulSoup(page, 'html.parser')
   # print(soup.prettify())
    title_tag = soup.title
    # 所有的超連結
    a_tags = soup.find_all('a')
    for tag in a_tags:
        # 輸出超連結
        links.append(str(tag.get('href')))
        # 輸出超連結的文字
        contextpool.append(str(tag.string).replace(' ','').replace(u'\u3000', '').replace(u'\xa0',''))

    div_tags = soup.find_all('div')
    for tag in div_tags:
    # 輸出DIV中的內文、並對其長度排序
        contextpool.append(str(tag.string).replace(' ', '').replace(u'\u3000', '').replace(u'\xa0', ''))

    h1_tags = soup.find_all('h1')
    for tag in h1_tags:
    # 輸出h1中的內文、並對其長度排序
        contextpool.append(str(tag.string).replace(' ', '').replace(u'\u3000', '').replace(u'\xa0', ''))
    
    contextpool.sort(key=cmp_to_key(lambda x, y: len(y)-len(x)))
    contextpool = list(dict.fromkeys(contextpool))
    print('------------')
    print('parser finish')
    if (title_tag == None):
        return '', contextpool, links
    return title_tag.string,contextpool,links


if __name__ == "__main__":
    parser('asdasfq')


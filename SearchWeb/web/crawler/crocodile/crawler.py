import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import re
pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')   # 合法網址的正則

times = 3                                        # 爬取網站的次數
DB = {}                                          # 放入 elastic search 的資料，DB[URL] = 連結文字
SearchDB = ["http://www.ccu.edu.tw"]             # 存放可以爬取的 URL，起始爬取網站是 http://www.ccu.edu.tw
DB["http://www.ccu.edu.tw"] = "國立中正大學"      # 賦予 DB 的起始值


# while len(SearchDB) > 0 :                      # 循環直到 Search 的長度為零
while times > 0 :                                # 循環直到 times 的值為零
    
    target = SearchDB[0]                         # 取出當次欲爬取的 URL
    print("target :", target)
    
    r = requests.get(target)                     # 向該 URL 發出 get 請求
    soup = BeautifulSoup(r.text, "html.parser")
    sel = soup.select("a")                       # 取出網頁中所有 <a> 標籤的內容

    URLS = []                                    # 暫存當次所爬取的 URL
    dict = {}                                    # 暫存當次所爬取的資料，dict[URL] = 連結文字
    for s in sel:                                # 取出每一個 <a> 標籤
        if(s.has_attr('href')):                  # 判斷是否具有 href 屬性
            # print(s["href"], s.text)

            url = re.findall(pattern, urljoin(target, s["href"]))     # 將相對網址轉成絕對網址後，接著判斷網址是否合法
            if url:                                                   # 若存在合法網址，將其存入資料結構
                # print(url[0])
                dict[url[0]] = s.text.replace("\n", " ")              # 去除連結文字的 '\n' 和存入資料結構

    URLS = list(dict.keys())
    print("dict :", len(dict), ",", "URLS :", len(URLS))



    import time
    import urllib.request
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/49.0.2')]

    count = 0
    for i in URLS:                               # 檢查收集到的網址是否可以對其發出請求並得到正常的回應
        tempUrl = i
        # print(tempUrl)
        try :
            opener.open(tempUrl)
            # print(tempUrl + ' - 沒問題')
        except urllib.error.HTTPError:
            print(tempUrl + ' - 訪問頁面出錯_1')
            gc = dict.pop(tempUrl, None)         # 收到錯誤回應後，從資料中去除該 URL 
            time.sleep(1)
        except urllib.error.URLError:
            print(tempUrl + ' - 訪問頁面出錯_2')
            gc = dict.pop(tempUrl, None)         # 收到錯誤回應後，從資料中去除該 URL 
            time.sleep(1)
        time.sleep(0.1)
        count += 1
    print("總共測試的網址 :", count)

        
    
    print("dict :", len(dict))
    # print(dict.keys())

    for i in dict.keys():                        # 取出每一個網址
        DB[i] = dict[i]                          # 將暫存的 URL 和連結文字存入即將放入 elastic search 的資料結構
        SearchDB.append(i)                       # 將暫存的 URL 存入下次可以爬取 URL 的資料結構
    
    dup = set(SearchDB)                          # 去除重複的 URL
    SearchDB = list(dup)
    SearchDB.remove(target)                      # 去除已搜尋的 URL
    
    print("DB :", len(DB))
    print("SearchDB :", len(SearchDB))
    times -= 1

    
print(DB)
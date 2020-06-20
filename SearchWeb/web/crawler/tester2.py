# from urllib.parse import urlparse

import requests

# url='https://tw.news.yahoo.com/'
# parseURL = urlparse(url).netloc.split('.')
# print(parseURL)
# for i in range(3):
#     print(len(urlparse(url).netloc.split('.', 3)[i]))
#     if (len(urlparse(url).netloc.split('.', 3)[i]) > 63):
#         print(X)
import ElasticSearchDB_ctrl
import DatabaseCtrl
import DataStruct
currentUrl='http://ce.naer.edu.tw/getfile.php?type=media&pattern=Q2VVcmxeX144M15fXm10eXBlPW1lZGlhJmRldGFpbD04Mw%3D%3D'
#a = ElasticSearchDB_ctrl.Elasticsearch_IPDB()
try:
     url = currentUrl
except UnicodeEncodeError:
     print(UnicodeEncodeError)
     #     return DataStruct.fetchData(time=theTime,status_code=99999,url=url)

try:
    response = requests.get(currentUrl, timeout=5, verify=False)
    print('success')
    print(response)

except requests.exceptions.RequestException as e:
    print(e)
#a.getAllData()
# DatabaseCtrl.filterArrInsert(['123'])
# DatabaseCtrl.filterArrInsert(['123'])

# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrInsert(['123'])
# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrDelete(['123'])
# DatabaseCtrl.filterArrDelete(['123'])

# DatabaseCtrl.failURLDBinsert(['failurl','from','errcode1'], 1)
# DatabaseCtrl.failURLDBinsert(['failurl','from','errcode2'], 1)
# DatabaseCtrl.failURLDBinsert(['failurl','from','errcode3'],1)
# k = DatabaseCtrl.failURLDBget(1)
# for i in k:
#     print(i)

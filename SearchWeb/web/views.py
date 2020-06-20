from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from datetime import datetime

import pandas as pd
import csv
import json
from .crawlermanage import crawlermanage
from .crawler.DatabaseCtrl import mutual_stateDBinsert
from .crawler.DatabaseCtrl import currentBatchGet
from .crawler.ElasticSearchDB_ctrl import Elasticsearch_IPDB
from .crawler.DatabaseCtrl import urlqueueDBget
from .crawler.DatabaseCtrl import failURLDBget
from .crawler.DatabaseCtrl import filterArrGet
from .crawler.DatabaseCtrl import filterArrDelete
from .crawler.DatabaseCtrl import filterArrInsert

from .crawler.DataStruct import IPData
def Search(request):
    return render(request, 'index.html')

def Dashboard(request):
    if 'newthread-URL' in request.POST:
        print("url:" + request.POST['newthread-URL'])
        print("level:" + request.POST['newthread-level'])
        print("wait:" + request.POST['newthread-wait'])
        print("num:" + request.POST['newthread-num'])
        print("state:" + request.POST['newthread-state'])
        datas = [request.POST['newthread-num'], request.POST['newthread-state'], request.POST['newthread-URL'], request.POST['newthread-URL'], request.POST['newthread-level'], request.POST['newthread-wait']]
        #mutual_stateDBinsert(datas)
        return render(request, 'dashboard.html')
    else:
        return render(request, 'dashboard.html')

def Page(request, searchText, page):
	return render(request, 'index.html', {
        'searchText': searchText,
        'page': page
    })

def GetBatchCsv(request):
    all_lines = ''
    for i in range(1, 5):
        all_lines=all_lines+','.join(currentBatchGet(i))+'\n'
    print(all_lines)
    return HttpResponse(all_lines, content_type="text/csv")


def GetMutualState(request):
    all_lines=[]
    with open('web\crawler\mutual_state.csv','r', newline='',encoding="utf-8") as fp1:
        all_lines = all_lines + fp1.readlines()
    print(all_lines)
    return HttpResponse(all_lines, content_type="text/csv")



def ReadDB(request):
	contentDB = pd.read_csv('web\crawler\contentDB.csv',index_col=0)
	print(contentDB)

	for row in contentDB.iterrows():
		print(row[1].URL)
		print(row[1].content)
		print(row[1].title)

	return render(request, 'null.html', {
        'data': contentDB,
    })

from django.template.context_processors import csrf
from django.http import JsonResponse

def get_csrf(request):
        #生成 csrf 数据，发送给前端
    x = csrf(request)
    csrf_token = x['csrf_token']
    data = {
        'csrf_token': str(csrf_token),
    }
    return JsonResponse(data)

def GetBanInDB(request):
    b = Elasticsearch_IPDB()
    banArr = b.banInDB()
    result=''
    for i in range(len(banArr)):
        result=result+banArr[i]+'\n'
    return HttpResponse(result, content_type="text/csv")

def isIpV4AddrLegal(ipStr):
    # 切割IP地址为一个列表
    ip_split_list = ipStr.strip().split('.')
    # 切割后列表必须有4个元素
    if 4 != len(ip_split_list):
        return False
    for i in range(4):
        try:
            # 每个元素必须为数字
            ip_split_list[i] = int(ip_split_list[i])
        except:
            print("IP invalid:" + ipStr)
            return False
    for i in range(4):
        # 每个元素值必须在0-255之间
        if ip_split_list[i] <= 255 and ip_split_list[i] >= 0:
            pass
        else:
            print("IP invalid:" + ipStr)
            return False
    return True

def insertBanInDB(request):
    ip=request.GET['insertBanIp']
    b = Elasticsearch_IPDB()
    result = ''
    if (isIpV4AddrLegal(ip)):
        ipID = b.CheckIPinDB(ip)
        print(ipID)
        if (ipID != 'NotInIPDB'):
            Bdata=IPData(ip=ip,isban=1)
            b.updateDBisban(ipID, Bdata)
    return HttpResponse(result, content_type="text/csv")

def deleteBanInDB(request):
    ip=request.GET['deleteBanIp']
    b = Elasticsearch_IPDB()
    print('--------------')
    print(ip)
    print(isIpV4AddrLegal(ip))
    print('--------------')
    result = ''
    if (isIpV4AddrLegal(ip)):
        ipID = b.CheckIPinDB(ip)
        print('--------------')
        print(ipID)
        print('--------------')

        if (ipID != 'NotInIPDB'):
            Bdata=IPData(ip=ip,isban=0)
            b.updateDBisban(ipID, Bdata)
    return HttpResponse(result, content_type="text/csv")
    
def getURLQueue(request):
    thread = request.GET['thread']
    data = urlqueueDBget(int(thread))
    result = ''
    z=0
    if len(data) > 100:
        z = 100
    else:
        z=len(data)
    for i in range(z):
        result =result+ ','.join(data[i])+'\n'
    return HttpResponse(result, content_type="text/csv")

def getFailURL(request):
    thread = request.GET['thread']
    data = failURLDBget(thread)
    result = ''
    for i in range(len(data)):
        result =result+ ','.join(data[i])+'\n'
    return HttpResponse(result, content_type="text/csv")

def getFilter(request):
    result = ''
    data = filterArrGet()
    for i in range(len(data)):
        result =result+ ','.join(data[i])+'\n'
    return HttpResponse(result, content_type="text/csv")

def deleteFilter(request):
    data = request.GET['data']
    result =filterArrDelete([data])
    return HttpResponse(result, content_type="text/csv")

def insertFilter(request):
    data = request.GET['data']
    result =filterArrInsert([data])
    return HttpResponse(result, content_type="text/csv")

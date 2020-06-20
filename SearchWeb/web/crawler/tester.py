import ElasticSearchDB_ctrl
import DatabaseCtrl
import DataStruct
a = ElasticSearchDB_ctrl.Elasticsearch_siteDB()
a.deleteDB()
a.newSiteDB()
# #a.searchDB('中正')
# #print(DatabaseCtrl.urlqueueDBget(1))
# #print(a.CheckDBUrl('https://www.ccu.edu.tw/'))
# #DatabaseCtrl.urlqueueDBinsert([['adasdm,2'], ['dasda,3']], 1)
# #DatabaseCtrl.urlqueueDBdelete(1)

b = ElasticSearchDB_ctrl.Elasticsearch_IPDB()
b.deleteDB()
b.newIPDB()
for i in range(1, 5):
    DatabaseCtrl.resetSeenDB(i)
    DatabaseCtrl.resetFailURLDB(i)
    DatabaseCtrl.currentBatchInsert(['0.0.0.0', '', 0, 0, 0, 0, 0, 0, 0, 0], i)

# DataStruct.currentBatch()
# #IP,????,????,???,????,???,???,??URL?,??,????



# while (1):
#     DatabaseCtrl.LockSeenDB()
#     if (DatabaseCtrl.isSeenDBLock() == 1):
#         print(1)
#         DatabaseCtrl.UnlockSeenDB()
    

# # data = DataStruct.IPData(ip='0.0.0.1',isban=1)
# # b.insertDataToDB(data)
# # data = DataStruct.IPData(ip='0.0.0.2',isban=1)
# # b.insertDataToDB(data)
# # data = DataStruct.IPData(ip='0.0.0.3',isban=1)
# # b.insertDataToDB(data)
# print(b.banInDB())

# ipID = b.CheckIPinDB('0.0.0.0')
# print(ipID)
# if (ipID != 'NotInIPDB'):
#     print(b.getIDdata(ipID).url)
#     Bdata=DataStruct.IPData(url='second',isban=0,speed=0.10)
#     b.updateDB(ipID, Bdata)
#     print(b.getIDdata(ipID).isban)
# SeenDB=DatabaseCtrl.loadSeenDB()
# isindb, seendb, k = DatabaseCtrl.checkinSeenDB('https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=otc', SeenDB)
# isindb,seendb,k=DatabaseCtrl.checkinSeenDB('https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=otc',SeenDB)
# isindb,seendb,k=DatabaseCtrl.checkinSeenDB('https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=otc',SeenDB)
# isindb,seendb,k=DatabaseCtrl.checkinSeenDB('https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=otc',SeenDB)
# isindb,seendb,k=DatabaseCtrl.checkinSeenDB('https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=otc',SeenDB)
# isindb,seendb,k=DatabaseCtrl.checkinSeenDB('https://tw.stock.yahoo.com/d/i/rank.php?t=pri&e=otc',SeenDB)

# DatabaseCtrl.updateSeenDB(seendb)


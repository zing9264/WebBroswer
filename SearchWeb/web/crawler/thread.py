import subprocess
import os
import sys
import time
import csv

print(os.path.dirname(__file__))
path = "workon django && python " + os.path.dirname(__file__) + "\crawler.py"
print(path)

set = [0,0,0,0]

#p = subprocess.Popen(path, shell=True)
#p2 = subprocess.Popen(path, shell=True)
#p3 = subprocess.Popen(path, shell=True)
#p4 = subprocess.Popen(path, shell=True)

#p5 = subprocess.Popen("workon django && python crawler.py", shell=True)
#p6 = subprocess.Popen("dir", shell=True)

#p.terminate()
#p2.terminate()
#p3.terminate()

while 1:

	with open('mutual_state.csv', newline='') as csvfile:
	# 讀取 CSV 檔案內容
		reader = csv.reader(csvfile)
		print(reader)
		rows = [row for row in reader]

		print(rows[1][1])
		print(rows[2][1])
		print(rows[3][1])
		print(rows[4][1])
		
		if set[0]==0 and rows[1][1]=="run":
			#p.terminate()
			p = subprocess.Popen(path, shell=True)
			set[0] = 1
		elif set[1]==0 and rows[2][1]=="run":
			p2 = subprocess.Popen(path, shell=True)
			set[1] = 1
		elif set[2]==0 and rows[3][1]=="run":
			p3 = subprocess.Popen(path, shell=True)
			set[2] = 1
		elif set[3]==0 and rows[4][1]=="run":
			p4 = subprocess.Popen(path, shell=True)
			set[3] = 1
		
		if set[0] and rows[1][1]=="delete":
			#p.terminate()
			subprocess.call(['taskkill', '/F', '/T', '/PID',  str(p.pid)])
			set[0] = 0
		elif set[1] and rows[2][1]=="delete":
			subprocess.call(['taskkill', '/F', '/T', '/PID',  str(p2.pid)])
			set[1] = 0
		elif set[2] and rows[3][1]=="delete":
			subprocess.call(['taskkill', '/F', '/T', '/PID',  str(p3.pid)])
			set[2] = 0
		elif set[3] and rows[4][1]=="delete":
			subprocess.call(['taskkill', '/F', '/T', '/PID',  str(p4.pid)])
			set[3] = 0
		
	time.sleep(2)
	
	if set[0]==0 and set[1]==0 and set[2]==0 and set[3]==0:
		break

#retcode = p.wait()
#retcode = p2.wait()
#retcode = p3.wait()
#retcode = p4.wait()

with open('mutual_state.csv', newline='') as csvfile:
	reader = csv.reader(csvfile)
	rows = [row for row in reader]
	
	rows[5][0] = "0"
	
	writer = csv.writer(open('mutual_state.csv', 'w', newline=''))
	writer.writerows(rows)

print("crawler finish")


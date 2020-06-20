from channels.generic.websocket import WebsocketConsumer
from .crawler.DatabaseCtrl import currentBatchGet
from .crawler.DatabaseCtrl import currentBatchInsert
import json
import os
import subprocess
import csv
import time
#import logging

# logging module with django logging
#logger = logging.getLogger('django')

class Consumer(WebsocketConsumer):
	def connect(self):
		self.accept()
		print('connect')
		#logger.debug('connect')

	def disconnect(self, close_code):
		pass

	def receive(self, text_data):
		print('send')
		text = "activate"
		#time.sleep(1)
		#logger.debug('send')
		print(os.path.dirname(__file__))
		data = json.loads(text_data)
		print(data['URL'])
		print(data['Level'])
		print(data['Wait'])
		print(data['Num'])
		print(data['State'])
		Mu_path = os.path.join(os.path.dirname(__file__), 'crawler', 'mutual_state.csv')
		print(Mu_path)
		with open(Mu_path,'r', newline='') as csvfile:
			reader = csv.reader(csvfile)
			rows = [row for row in reader]
			i = int(data['Num'])
			print(rows)
			if ((data['Num'] != "1234") & (rows[5][0] == "0")&((data['State'] == "delete") |(data['State'] == "run")) ):
				rows[5][0] = "1"
				if rows[i][1] == "delete":
					rows[i][1] = data['State']
					rows[i][2] = data['URL']
					rows[i][3] = data['Level']
					rows[i][4] = data['Wait']
				writer = csv.writer(open(Mu_path, 'w', newline=''))
				writer.writerows(rows)
				path = os.path.join(os.path.dirname(__file__), 'crawler', 'thread.py')
				#path = "workon django && python " + path
				print(path)
				path = "conda activate py38 && python " + path
				p = subprocess.Popen(path, shell=True, cwd=os.path.join(os.path.dirname(__file__), 'crawler'))
			elif (data['State'] == "change_waittime"):
				rows[i][4] = data['Wait']
				arr = currentBatchGet(i)
				arr[8] = data['Wait']
				currentBatchInsert(arr,i)
				writer = csv.writer(open(Mu_path, 'w', newline=''))
				writer.writerows(rows)
			elif ( (rows[5][0] == "1")& (data['State'] == "close_crawler")):
				print('detect-rows[5][0] == 1')
				rows[1][1] = "delete"
				rows[2][1] = "delete"
				rows[3][1] = "delete"
				rows[4][1] = "delete"
				rows[5][0] = "0"
				writer = csv.writer(open(Mu_path, 'w', newline=''))
				writer.writerows(rows)
			elif ((rows[5][0] == "0") & (data['State'] == "close_crawler")):
				pass
			elif ((rows[5][0] == "1") & (data['State'] == "run") & (data['URL'] != '')):
				if rows[i][1] == "delete":
					rows[i][1] = data['State']
					rows[i][2] = data['URL']
					rows[i][3] = data['Level']
					rows[i][4] = data['Wait']
					writer = csv.writer(open(Mu_path, 'w', newline=''))
					writer.writerows(rows)
			elif((data['Num']!='1234')&(data['URL'] == '')&(data['Level'] == '')&(data['Wait'] == '')):
				print('modify'+Mu_path)
				rows[int(data['Num'])][1]=data['State']
				writer = csv.writer(open(Mu_path, 'w', newline=''))
				writer.writerows(rows)
			

		self.send(text_data=json.dumps({
			'message': text
		}))

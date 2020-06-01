from channels.generic.websocket import WebsocketConsumer

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
		#print(os.path.dirname(__file__))

		data = json.loads(text_data);
		#print(data['URL'])
		#print(data['Level'])
		#print(data['Wait'])
		#print(data['Num'])
		#print(data['State'])

		with open(os.path.join(os.path.dirname(__file__), 'crawler', 'mutual_state.csv'), newline='') as csvfile:
			
			reader = csv.reader(csvfile)
			rows = [row for row in reader]
			
			if rows[5][0]=="0":
			
				rows[5][0] = "1"
				
				i = 1
				count = 1
				while i<=4 and count<=int(data['Num']) and int(data['Num'])<=4 :
					
					if rows[i][1] == "delete":
						rows[i][1] = data['State']
						rows[i][2] = data['URL']
						rows[i][3] = data['URL']
						rows[i][4] = data['Level']
						rows[i][5] = data['Wait']
						count = count + 1
					i = i + 1
					
				writer = csv.writer(open(os.path.join(os.path.dirname(__file__), 'crawler', 'mutual_state.csv'), 'w', newline=''))
				writer.writerows(rows)

				path = os.path.join(os.path.dirname(__file__), 'crawler', 'thread.py')
				path = "workon django && python " + path
				p = subprocess.Popen(path, shell=True, cwd=os.path.join(os.path.dirname(__file__), 'crawler'))
				
			else:
				text = "running"
		
		self.send(text_data=json.dumps({
			'message': text
		}))
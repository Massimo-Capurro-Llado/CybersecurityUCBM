import http.client
import json
import time

while(True):
	conn = http.client.HTTPConnection('10.0.0.3', 80)
	conn.request('GET', '/')

	response = conn.getresponse()
	string = response.read().decode('utf-8')
	time.sleep(5)
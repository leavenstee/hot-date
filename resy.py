# RESY.PY
import requests
import urllib
import json
import datetime
import time
import schedule

'''
1. get venue id DONE
2. hit slot query -> save config.id DONE
3. Send Config ID DONE
4. Save book_token.value DONE
5. send book request
'''
def job():
	print "Start Booking"

	headers = {
	'origin': 'https://resy.com',
	'accept-encoding': 'gzip, deflate, br', 
	'x-origin': 'https://widgets.resy.com', 
	'accept-language': 'en-US,en;q=0.9',
	'authorization': 'ResyAPI api_key="VbWk7s3L4KiK5fzlO7JD3Q5EYolJI7n5"', 
	'pragma': 'no-cache', 
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', 
	'content-type': 'application/x-www-form-urlencoded', 
	'accept': 'application/json, text/plain, */*', 
	'cache-control': 'no-cache', 
	'authority': 'api.resy.com', 
	'referer': 'https://resy.com'
	 }
	userAuthToken = '_TN2OF4tvzHd71vYi5T8ubLsWY|HNBDv0_qGCWBeK1joDZ_Xaf_9Cp0_E_taDJV6t0c6WUIEVsIK1MYD68s06aondG9_jgGloIdwZeYmgQw=-0f98cc084fd6b4277ddd058d1d69fb161e509e2bb3c3064056a71b2b'
	weakAuthToken = 'yDFWhG7_KneKK2Nj9veohXnEgZu3XuF0DT491IVN5i17tXJ1nkj6pFV3e0ENb5dZwql2zPtr3naMS4ouSahntMNsAVcNUg7zeLcGyhJhoBo%3D-22a7adfc292b099c1b96db135119bac50da983bd58bc8f9ae791fede'

	### Set Venue ID ###
	date = '2018-10-23'
	latatude = 0
	longatude = 0
	partySize = 4
	venueID = 418

	slotURL = 'https://api.resy.com/4/find?'
	slotData = [
		('auth_token', weakAuthToken),
		('day', date),
		('lat', latatude),
		('long', longatude),
		('party_size', partySize),
		('venue_id', venueID)
		]

	slotDataString = urllib.urlencode(slotData)
	slotDataString = slotDataString.replace("%25", "%") #fix encoding percent bug 
	slotURL = slotURL + slotDataString # Concat Stirng Builder

	### Send Slot Query Request & Save Config ID ###
	response = requests.get(slotURL, headers=headers)
	jsonData = response.json()

	### Collection of config ideas
	configIDs = []

	sevenPM = datetime.datetime(2018, 10, 23, 19, 00)
	ninePM = datetime.datetime(2018, 10, 23, 21, 00)

	for i in jsonData["results"]["venues"][0]["slots"]:
		resDataTime = i["date"]["start"] 

		datetime_object = datetime.datetime.strptime(resDataTime, '%Y-%m-%d %H:%M:%S')
		
		if sevenPM < datetime_object:
			if ninePM > datetime_object:
				configIDs.append(i["config"]["id"])
	print "config id gathered"			
		
	if len(configIDs) > 0:
		### Now we have config ids we need to send 
		configURL = 'https://api.resy.com/3/details?'
		configData = [
			('auth_token', weakAuthToken),
			('config_id', configIDs[0]),
			('day', date),
			('party_size', partySize)
			]

		configDataString = urllib.urlencode(configData)
		configDataString = configDataString.replace("%25", "%") #fix encoding percent bug 
		configURL = configURL + configDataString # Concat Stirng Builder

		response = requests.get(configURL, headers=headers)
		jsonData = response.json()

		if "book_token" not in jsonData:
			print "No RESY for you"
		else:
			book_token = jsonData["book_token"]["value"]



			### Book The damn thing
			bookURL = "https://api.resy.com/3/book"

			bookData = {
				'auth_token': userAuthToken,
				'book_token': book_token, 
				'source_id': 'resy.com-reservations'
				}

			response = requests.post(bookURL, headers=headers, data=bookData)
			print response.text
	else:
		print "no config ids for today"

schedule.every().day.at("23:01").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
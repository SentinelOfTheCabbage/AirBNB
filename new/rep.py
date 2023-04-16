import MySQLdb
import json
import os
db = MySQLdb.connect(host="localhost",  # your host 
                     user="root",       # username
                     passwd="password",     # password
                     db="AirBNB")   # name of the database
folder = '/home/neil/git_workspace/get_airbnb/120819'
query = 'INSERT INTO price_table_new VALUES '
for i in range(41):
	cur_folder = folder + '/{}/'.format(i)
	with open(cur_folder + 'id_list.json','r') as file:
		id_list = json.loads(file.read())
	for room in id_list:
		if os.path.exists(cur_folder + str(room['id'])):
			info_file = cur_folder + '{}/CZK.json'.format(room['id'])
			with open(info_file,'r') as file:
				room_info = json.loads(file.read())
			cur_cf = 0
			price_info = room_info['pdp_listing_booking_details'][0]['price']['price_items']
			for j in price_info:
				if j['type'] == 'CLEANING_FEE':
					cur_cf = j['total']['amount']
			query += '({},{},{},{}),'.format(room['id'],cur_cf,room['disc_m'], room['disc_w'])

query =query[:-1]
print(query)
cu = db.cursor()
cu.execute(query)
db.commit

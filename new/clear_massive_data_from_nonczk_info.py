import os
import json

path = '/home/neil/git_workspace/get_airbnb/190812/'
def remove_if_exists(room_path,filename):
	file_path = room_path+filename
	if os.path.exists(file_path):
		os.remove(file_path)

for i in range(41):
	filename = path + '{}/id_list.json'.format(i)
	with open(filename,'r') as file:
		id_list = json.loads(file.read())
	for room in id_list:
		room_path = path+'{}/{}/'.format(i,room['id'])
		if os.path.exists(room_path):
			remove_if_exists(room_path, 'C_EUR.json')
			remove_if_exists(room_path, 'C_RUB.json')
			remove_if_exists(room_path, 'C_USD.json')
			remove_if_exists(room_path, 'RUB.json')
			remove_if_exists(room_path, 'USD.json')
			remove_if_exists(room_path, 'EUR.json')
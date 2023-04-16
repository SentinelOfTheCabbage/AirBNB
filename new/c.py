import os
import json
count = 0
result = {}
for day in range(30):
	global_path = '{}0919/'.format(str(day))
	if os.path.exists(global_path):
		print('d_{}'.format(day))
		count += 1
		for folder in range(41):
			folder_path = global_path + '{}/'.format(folder)
			with open(folder_path + 'id_list.json','r') as file:
				id_list = json.loads(file.read())
			for room_id in id_list:
				id = room_id['id']
				room_path = folder_path + str(id) + '/'
				file_path = room_path + 'C_CZK.json'
				if os.path.exists(room_path):
					with open(file_path,'r') as file:
						room = json.loads(file.read())
				else:
					continue
				if room['calendar_months'][0]['days'][day-1]['available'] is False:
					if id in list(result.keys()):
						result[id] += 1
					else:
						result[id] = 1
						
res = {str(value): int(100*result[value]/count) for _, value in enumerate(result)}
print(count)

with open('w8.json','w') as f:
	f.write(str(res))
import json
import os
with open('R_new.json','r') as file:
	all_data = json.loads(file.read())
count = 0
path = ''
while len(all_data)>300:
	path = 'R/{}/'.format(count)
	if not os.path.exists(path):
		os.mkdir(path)
	with open(path+'id_list.json','w') as f:
		f.write(str(all_data[:300]).replace("'",'"').replace('None','null'))
		count += 1
		all_data = all_data[300:]


path = 'R/{}/'.format(count)
if not os.path.exists(path):
	os.mkdir(path)
with open(path+'id_list.json','w') as f:
	f.write(str(all_data).replace("'",'"').replace('None','null'))
	count += 1


# import json
# all_data = []
# for i in range(12):
# 	with open('X/x_'+str(i)+'.json','r') as f:
# 		current_file = f.read()
# 	cur_data = json.loads(current_file)
# 	all_data += cur_data
# print(len(all_data))
# # id_list = []
# # for i in all_data:
# # 	id_list.append(i['id'])
# # result = []
# # for pos,value in enumerate(id_list):
# # 	if not (value in id_list[pos+1:]):
# # 		result.append(all_data[pos])
# # with open('R.json','w') as f:
# # 	f.write(str(result).replace("'",'"'))
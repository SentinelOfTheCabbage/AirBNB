import os
from datetime import datetime
import json

prev_route = 'git_workspace/get_airbnb/'+input('Previous route: ')
new_route = 'git_workspace/get_airbnb/'+input('New route: ')

for i in range(41):
	cur_prev_directory = prev_route + '/{}'.format(i)
	cur_new_directory = new_route + '/{}'.format(i)

	with open (cur_new_directory,'r') as file:
		homes_id_list = json.loads(file.read())
	for home in homes_id_list:
		cur_id = home['id']
		
		prev_calendar_filename = cur_prev_directory + '/{}'.format(cur_id)
		new_calendar_filename = cur_new_directory + './{}'.format(cur_id)
		
		if not (os.path.exists(prev_calendar_filename) and os.path.exists(new_calendar_filename)):
			continue

		with open(prev_calendar_filename+'C_CZK.json') as file:
			prev_calendar = json.loads(file.read())['calendar_months']
		with open(new_calendar_filename+'C_CZK.json') as file:
			new_calendar = json.loads(file.read())['calendar_months']
		for i in 
statbuf = os.stat(filename)
mdate = datetime.fromtimestamp(statbuf.st_mtime).strftime('%Y-%m-%d')
print('Modification time {}'.format(mdate))
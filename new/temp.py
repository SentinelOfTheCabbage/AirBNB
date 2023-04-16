for i in range(41):
	filename ='R/'+ str(i) + '/id_list.json'
	with open(filename,'r') as file:
		content = file.read()
	content.replace('"null"','null')
	print(content)
	with open(filename, 'w') as file:
		file.write(content)
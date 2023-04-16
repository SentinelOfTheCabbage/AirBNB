import requests
import os
import json
from datetime import datetime
class ParseAirBNB():

	def save_to_json(self, path, filename, source):
		filename = '{}.json'.format(filename)
		if not os.path.exists(path):
			os.makedirs(path)

		with open(path+'/'+filename,'w') as file:
			file.write(source)		

	def get_main_pages(self,country,city):
		page_pattern = 'https://www.airbnb.ru/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&currency=RUB&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset={}&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&luxury_pre_launch=true&metadata_only=false&place_id=ChIJi3lwCZyTC0cRkEAWZg-vAAQ&query={},{}&query_understanding_enabled=true&refinement_paths[]=/homes&s_tag=4EYZVohU&satori_version=1.1.9&search_type=pagination&section_offset=7&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=180&version=1.5.8'
		pages_count=0
		id_set = set()
		flag = True
		last_page = False
		while (flag is True) or (last_page is True):
			current_page = page_pattern.format(pages_count*50,city,country)
			main_pages_json = requests.get(current_page).text
			path = '/'.join([country,city])

			self.save_to_json(path,'main_'+str(pages_count),main_pages_json)
			id_set.update(self.get_all_rooms_json(path,main_pages_json))				

			if last_page is True:
				self.save_to_json(path,'main_'+str(pages_count),main_pages_json)
				break

			flag = json.loads(main_pages_json)['explore_tabs'][0]['pagination_metadata']['has_next_page']
			pages_count += 1

			if flag is False:
				last_page = True
		self.save_set(path,id_set)
		self.save_all_rooms(path,id_set)

	def save_set(self,path,id_set):
		content = str(list(id_set))
		self.save_to_json(path,'id_list',content)

	def save_all_rooms(self,path,id_set):
		count = 0
		for id in id_set: 
			percent = count/306*100
			table = ['■ ' for i in range(round(percent/5))] +['▢ ' for i in range(20-round(percent/5))]
			move(2,0)
			print('[{}]'.format(''.join(table)))
			print('{}%[{}]'.format(round(percent,2),datetime.now()-startTime))
			count += 1
			self.get_room_json_from_html(path,id)
			self.get_room_json_calendar(path,id)
			self.get_room_review_jsons(path,id)

	def get_all_rooms_json(self,path,main_pages_json):
		id_set = set()
		listings = json.loads(main_pages_json)['explore_tabs'][0]['sections'][0]['listings']
		for i in listings:
			id_set.add(i['listing']['id'])
		return id_set

	def get_room_review_jsons(self,path,id):
		 path = '{}/{}'.format(path,id)
		 url = 'https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&_format=for_p3&limit={}&offset=0&order=language_country'
		 reviews_count = int(json.loads(requests.get(url.format(id,1)).text)['metadata']['reviews_count'])
		 url = 'https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&_format=for_p3&limit={}&offset=0&order=language_country'
		 review_source = requests.get(url.format(id,reviews_count)).text
		 self.save_to_json(path,'reviews',review_source)

	def get_room_json_calendar(self,path,id):
		url = 'https://www.airbnb.ru/api/v2/homes_pdp_availability_calendar?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&month=7&year=2019&count=12'
		content = requests.get(url.format(id)).text
		path = '{}/{}'.format(path,id)
		self.save_to_json(path, 'calendar', content)


	def get_room_json_from_html(self,path,id):
		path = path + '/' + str(id)
		content = requests.get('https://www.airbnb.ru/rooms/{}'.format(id)).text
		content = content[content.find('data-state'):content.rfind('data-apollo-state')]
		content = content[content.find('<!--'):content.rfind('-->')]
		content = content[4:]
		self.save_to_json(path,'html',content)
		# String content = Jsoup.connect(mainPageUrl).get().html();
        # String JSON = content.substring(content.indexOf("data-state"),content.lastIndexOf("data-apollo-state"));
        # JSON = JSON.substring(JSON.indexOf("<!--"),JSON.lastIndexOf("-->"));
        # JSON = JSON.substring(4);

def move (y, x):
    print("\033[%d;%dH" % (y, x))

startTime = datetime.now()
X = ParseAirBNB().get_main_pages('Россия','Москва')
print(datetime.now() - startTime)
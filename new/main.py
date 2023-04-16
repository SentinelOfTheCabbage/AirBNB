import requests
import os
import json
import sys
from datetime import datetime
import time
class ParseAirBNB():

    # def __init__(self, country,city):
    #     path = '{}/{}'.format(country,city)
    #     with open(path+'/id_list.json') as source:
    #         id_list = source.read();
    #     id_json = json.loads(id_list)

    #     url_pattern = 'https://www.airbnb.ru/api/v2/homes_pdp_availability_calendar?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&month=8&year=2019&count=12'
    #     for i in id_json:
    #         content = request((url_pattern.format(i['id'])).text
    #         cur_path = '{}/{}'.format(path, i['id'])
    #         self.save_to_json(cur_path, 'calendar', content)


    def save_to_json(self, path, filename, source):
        filename = '{}.json'.format(filename)
        if not os.path.exists(path):
            os.makedirs(path)

        with open(path+'/'+filename,'w') as file:
            file.write(source)

    def get_main_pages(self,country,city):
        page_pattern = 'https://www.airbnb.ru/api/v2/explore_tabs?_format=for_explore_search_web&_intents=p1&auto_ib=false&currency=RUB&experiences_per_grid=20&fetch_filters=true&guidebooks_per_grid=20&has_zero_guest_treatment=true&is_guided_search=true&is_new_cards_experiment=true&is_standard_search=true&items_offset={}&items_per_grid=50&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&luxury_pre_launch=true&metadata_only=false&place_id=ChIJi3lwCZyTC0cRkEAWZg-vAAQ&query={},{}&query_understanding_enabled=true&refinement_paths[]=/homes&s_tag=4EYZVohU&satori_version=1.1.9&search_type=pagination&section_offset=7&selected_tab_id=home_tab&show_groupings=true&supports_for_you_v3=true&timezone_offset=180&version=1.5.8'
        pages_count=0
        self.id_set = []
        flag = True
        last_page = False
        while (flag is True) or (last_page is True):
            current_page = page_pattern.format(pages_count*50,city,country)
            main_pages_json = request(current_page).text
            # print(current_page)
            path = '/'.join([country,city])

            self.save_to_json(path,'main_'+str(pages_count),main_pages_json)
            self.id_set = self.id_set + self.get_all_rooms_json(path,main_pages_json)

            if last_page is True:
                self.save_to_json(path,'main_'+str(pages_count),main_pages_json)
                break

            flag = json.loads(main_pages_json)['explore_tabs'][0]['pagination_metadata']['has_next_page']
            pages_count += 1

            if flag is False:
                last_page = True
        self.save_set(path)
        self.save_all_rooms(path,self.id_set)
        self.save_datastamp(path)

    def save_set(self,path):
        content = str(list(self.id_set)).replace('\'','"')
        # [
        #   {id:,
        #    beds:
        #    bedrooms:,
        #    bathrooms:,
        #    guests:,
        #    coordinates:[lat,lng]
        #   }
        # ]
        self.save_to_json(path,'id_list',content)

    def save_all_rooms(self,path,id_set,room_id = None):
        if not room_id is None:
            id_setlist = [i['id'] for i in id_set]
            print(id_setlist)
            pos = id_setlist.index(int(room_id))
            print(pos)
            id_set = [id_set[pos]]
        count = 0
        for i in id_set:
            # percent = count/306*100
            # move(2,0)
            # print('[{}]'.format(''.join(table)))
            # print('{}%[{}]'.format(round(percent,2),datetime.now()-startTime))
            count += 1
            self.path = path
            self.id = i['id']
            # if os.path.exists('{}/{}'.format(self.path,self.id)):
            #     continue
            # url = 'https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&_format=for_p3&limit={}&offset=0&order=language_country'
            # content = request(url.format(self.id,1))
            # if content is None:
            #     continue
            self.get_room_json_from_html()
            # self.get_room_json_calendar()
            # self.get_room_json_prices()
            # self.get_room_review_jsons()
            # return 0

    def get_all_rooms_json(self,path,main_pages_json):
        id_set = []
        new_element = {}
        listings = json.loads(main_pages_json)['explore_tabs'][0]['sections'][0]['listings']
        for i in listings:
            new_element ={  'id':i['listing']['id'],
                            'bathrooms':i['listing']['bathrooms'],
                            'bedrooms':i['listing']['bedrooms'],
                            'beds':i['listing']['beds'],
                            'coordinates':{ 'lat':i['listing']['lat'],
                                            'lng':i['listing']['lng']
                                            }
                        }
            if not new_element in self.id_set:
                id_set.append(new_element)
        return id_set

    def get_room_review_jsons(self):
        path = '{}/{}'.format(self.path,self.id)
        url = 'https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&_format=for_p3&limit={}&offset=0&order=language_country'
        # print(url.format(self.id,1))
        content = request(url.format(self.id,1))
        if not content is None:
            reviews_count = json.loads(content.text).get('metadata', None)
            if reviews_count is None:
                print (url.format(self.id,1))
                reviews_count = 0
            else:
                reviews_count = reviews_count['reviews_count']
            url = 'https://www.airbnb.ru/api/v2/homes_pdp_reviews?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&_format=for_p3&limit={}&offset=0&order=language_country'
            review_source = request(url.format(self.id,reviews_count))
            # if not review_source is None:
            #     content = content.text
            self.save_to_json(path,'reviews',review_source.text)

    def get_room_json_calendar(self):
        path = '{}/{}'.format(self.path,self.id)
        # if not os.path.exists('{}/{}.json'.format(path,'C_CZK')):
        #     return 0
        # url = 'https://www.airbnb.ru/api/v2/homes_pdp_availability_calendar?currency=RUB&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&month=8&year=2019&count=12'
        # content = request(url.format(self.id)).text
        # self.save_to_json(path, 'C_RUB', content)
        # url = 'https://www.airbnb.ru/api/v2/homes_pdp_availability_calendar?currency=USD&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&month=8&year=2019&count=12'
        # content = request(url.format(self.id)).text
        # self.save_to_json(path, 'C_USD', content)
        # url = 'https://www.airbnb.ru/api/v2/homes_pdp_availability_calendar?currency=EUR&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&month=8&year=2019&count=12'
        # content = request(url.format(self.id)).text
        # self.save_to_json(path, 'C_EUR', content)
        url = 'https://www.airbnb.ru/api/v2/homes_pdp_availability_calendar?currency=CZK&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&locale=ru&listing_id={}&month=11&year=2019&count=12'
        content = request(url.format(self.id))
        if not content is None:
            content = content.text
        else:
            return 0
        self.save_to_json(path, 'C_CZK', content)


    def get_room_json_prices(self):
        path = '{}/{}'.format(self.path,self.id)
        if os.path.exists('{}/{}.json'.format(path,'CZK')):
            return 0
        # url = 'https://www.airbnb.ru/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&check_in=2011-11-11&check_out=2012-11-11&currency=RUB&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={}&locale=ru&number_of_adults=2&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
        # content = request(url.format(self.id)).text
        # self.save_to_json(path,'RUB',content)
        # url = 'https://www.airbnb.ru/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&check_in=2011-11-11&check_out=2012-11-11&currency=USD&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={}&locale=ru&number_of_adults=2&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
        # content = request(url.format(self.id)).text
        # self.save_to_json(path,'USD',content)
        # url = 'https://www.airbnb.ru/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&check_in=2011-11-11&check_out=2012-11-11&currency=EUR&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={}&locale=ru&number_of_adults=2&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
        # content = request(url.format(self.id)).text
        # self.save_to_json(path,'EUR',content)
        url = 'https://www.airbnb.ru/api/v2/pdp_listing_booking_details?_format=for_web_with_date&_intents=p3_book_it&_interaction_type=pageload&check_in=2011-11-11&check_out=2012-11-11&currency=CZK&force_boost_unc_priority_message_type=&guests=1&key=d306zoyjsyarp7ifhu67rjxn52tv0t20&listing_id={}&locale=ru&number_of_adults=2&number_of_children=0&number_of_infants=0&show_smart_promotion=0'
        content = request(url.format(self.id))
        if not content is None:
            content = content.text
        else:
            return 0
        self.save_to_json(path,'CZK',content)


    def get_room_json_from_html(self):
        path = self.path + '/' + str(self.id)
        content = request('https://www.airbnb.ru/rooms/{}'.format(self.id))
        if not content is None:
            content = content.text
        else:
            return 0
        # content = content[content.find('data-state'):content.rfind('data-apollo-state')]
        # content = content[content.find('>'):content.rfind('</script>')]
        # content = content[1:]
        if not os.path.exists(path):
	        os.makedirs(path)
        with open('{}/content.html'.format(path),'w') as file:
        	file.write(content)
        # self.save_to_json(path,'html',content)

    def save_datastamp(self, path):
        filename = 'timestamp.txt'
        with open(path+'/'+filename,'w') as file:
            file.write(datetime.timestamp())


def request(url):
    while True:
        try:
            rs = requests.get(url)
            if rs.status_code != 200:
                print("Error Code:", rs.status_code)
                print('\tURL:',url)
                time.sleep(1)
                if (rs.status_code == 403):
                    return None
            else:
                return rs
        except ConnectionError:
            print("ConnectionError")
            time.sleep(1)
def move (y, x):
    print("\033[%d;%dH" % (y, x))

# startTime = datetime.now(
# for num in range(k,k+6):
#     startTime = datetime.now()
#     if num >0 :
#         current_city = city + ' ' + str(num)
#     else :
#         current_city = city

#     print('Start!')
#     X = ParseAirBNB(country,current_city)
#     print(num,' : ', datetime.now() - startTime)
k = sys.argv[1]
room_id = None
if len(sys.argv) == 3:
    room_id = sys.argv[2]
path = '/home/neil/git_workspace/get_airbnb/R/'+str(k)
print('Page #',str(k))
with open(path+'/id_list.json','r') as file:
    content = file.read()
id_set = json.loads(content)
ParseAirBNB().save_all_rooms(path,id_set, room_id)
# 20
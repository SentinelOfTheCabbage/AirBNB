import requests
import json
from time import sleep
class ParseOneMainPage():
    def get_pages_as_list(self,street_name):
        id_list = []
        places_and_queries = self.get_place_id(street_name)
        if len(places_and_queries)>0:
            for i in places_and_queries:
                tabs_url = self.get_tabs_url(i['place_id'],i['query'])
                new_id_list = self.get_info_list(tabs_url,street_name)
                id_list += new_id_list
        return id_list

    def get_info_list(self,tabs_url,street_name):
        info_list = []
        flag = True
        last_page = False
        readed = 0
        rooms_count = self.get_rooms_count(tabs_url)
        if (rooms_count>=306):
            print('OVERFARM:', street_name)
        for i in range(int(rooms_count/50)+1):
            if rooms_count-readed<50:
                page_size = rooms_count - readed
            else:
                page_size = 50
            current_url = tabs_url.format(readed,page_size)
            page_content = self.get_connection(current_url).text
            source_json = json.loads(page_content)['explore_tabs'][0]['sections'][0].get('listings',None)
            if source_json == None:
                break
            for j in source_json:
                new_element = self.get_new_element(j)
                info_list.append(new_element)
            readed += 50
        return info_list

    def get_new_element(self, j_source):
        source = j_source['listing']
        new_element = {}
        new_element['id'] = source['id']
        new_element['bathrooms'] = source.get('bathrooms',None)
        new_element['bedrooms'] =source.get('bedrooms',None)
        new_element['beds'] = source.get('beds',None)
        new_element['disc_m'] = j_source['pricing_quote']['monthly_price_factor']
        new_element['disc_w'] = j_source['pricing_quote']['weekly_price_factor']
        new_element['coordinates'] = {'lat':source.get('lat',None),'lng':source.get('lng',None)}
        return new_element

    def get_connection(self, url):
        status_code = 0
        while (status_code != 200):
            r = requests.get(url)
            if r.status_code == 429:

                sleep(5)
                print('Z')
            status_code = r.status_code
        return r

    def get_rooms_count(self,pattern):
        url = pattern.format(1,1)
        page_content = self.get_connection(url).text
        current_json = json.loads(page_content)
        rooms_count = current_json['explore_tabs']
        rooms_count = rooms_count[0]['home_tab_metadata']['listings_count']
        return rooms_count

    def get_tabs_url(self,place_id,full_query):
        tabs_url = 'https://www.airbnb.ru/api/v2/explore_tabs?'
        tabs_url += '_format=for_explore_search_web&'
        tabs_url += '_intents=p1&'
        tabs_url += 'auto_ib=true&'
        tabs_url += 'currency=RUB&'
        tabs_url += 'experiences_per_grid=20&'
        tabs_url += 'fetch_filters=true&'
        tabs_url += 'guidebooks_per_grid=20&'
        tabs_url += 'has_zero_guest_treatment=true&'
        tabs_url += 'is_guided_search=true&'
        tabs_url += 'is_new_cards_experiment=true&'
        tabs_url += 'is_standard_search=true&'
        tabs_url += 'items_offset={}&'
        tabs_url += 'items_per_grid={}&'
        tabs_url += 'key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'
        tabs_url += 'locale=ru&'
        tabs_url += 'luxury_pre_launch=false&'
        tabs_url += 'metadata_only=false&'
        tabs_url += 'place_id={}&'.format(place_id)
        tabs_url += 'query={}&'.format(full_query)
        tabs_url += 'query_understanding_enabled=true&'
        tabs_url += 'refinement_paths[]=/homes&'
        tabs_url += 'satori_version=1.1.9&'
        tabs_url += 'search_type=unknown&'
        tabs_url += 'selected_tab_id=home_tab&'
        tabs_url += 'show_groupings=true&'
        tabs_url += 'supports_for_you_v3=true&'
        tabs_url += 'timezone_offset=180&'
        tabs_url += 'version=1.5.8'
        return tabs_url

    def get_place_id(self,street_name):
        result = []
        aut_url = self.get_aut_url(street_name + ', Прага')
        aut_content = self.get_connection(aut_url).text
        aut_json = json.loads(aut_content)['autocomplete_terms']
        del aut_content
        if len(aut_json) > 0:
            result = self.find_place_id(aut_json, street_name + ', ')
        if (len(aut_json) == 1) and (len(result) == 0):
            result = self.select_place_id(aut_json,street_name)
        elif len(result) == 0:
            print ('CAN\'T FIND STREET: ',street_name)
        return result

    def select_place_id(self,aut_json,street_name):
        answer = []
        i = aut_json[0]
        if street_name.lower() in i['explore_search_params']['query'].lower():
            answer.append({    'place_id':i['explore_search_params']['place_id'],
                        'query':i['explore_search_params']['query']})
        return answer

    def get_aut_url(self,street_name):
        aut_url = 'https://www.airbnb.ru/api/v2/autocompletes?'
        aut_url += 'country=GB&'
        aut_url += 'key=d306zoyjsyarp7ifhu67rjxn52tv0t20&'
        aut_url += 'language=ru&'
        aut_url += 'locale=ru&'
        aut_url += 'num_results=5&'
        aut_url += 'user_input={}&'.format(street_name)
        aut_url += 'api_version=1.1.9&'
        aut_url += 'vertical_refinement=all&'
        aut_url += 'options=should_show_stays'
        return aut_url

    def find_place_id(self, aut_json, street_name):
        answer = []
        if type(street_name) == type('hell'):
            street_name = [street_name]
        for i in aut_json:
            flag = True
            for j in street_name:
                if not j.lower() in i['explore_search_params']['query'].lower():
                    flag = False
                    break
            if flag is True:
                if (', Prague' in i['explore_search_params']['query']) or (', Прага' in i['explore_search_params']['query']):
                    answer.append({    'place_id':i['explore_search_params']['place_id'],
                                'query':i['explore_search_params']['query']})
        return answer

id_list=[]
Parser = ParseOneMainPage()
with open('cities.json','r') as file:
    content = file.read()
j_source = json.loads(content)
count = len(j_source)
n = 0
d = 0
for i in j_source:
    if round(n/count*100,4) < 0:
        n += 1
        if int(n/count*10) > d:
            d +=1
        continue
    print(j_source.index(i))
    if int(n/count*10) > d:
        d +=1
        with open('x.json','w') as f:
            f.write(content_to_file)

    print(round(n/count*100,4),'%')
    n +=1
    id_list += Parser.get_pages_as_list(i)
    content_to_file = str(id_list).replace('"','\"').replace("'",'"').replace('None','null')

# id_list += Parser.get_pages_as_list('28. pluk')
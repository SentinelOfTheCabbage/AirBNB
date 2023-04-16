import requests
from bs4 import BeautifulSoup
class StreetGetter():
	def __init__(self):
		cities_list = []
		H = self.get_url_array()
		for i in H:
			current_content = requests.get(i).content
			soup = BeautifulSoup(current_content,'lxml')
			samples = soup.find_all("a", class_ = "CategoryTreeLabelCategory")
			for j in samples:
				new_city = j.text
				if new_city.find(' (')>-1:
					new_city = new_city[:new_city.find(' (')]
					# new_city.rstrip();
				cities_list.append(new_city)
			print(i)
		with open('cities.json','w') as file:
			file.write(str(cities_list))
	def get_url_array(self):
		arr = [	'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatuntil=Bo%C5%BE%C3%ADdarsk%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Bo%C5%BE%C3%ADdarsk%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Do+Lipin#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Hadovit%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Jalovcov%C3%A1+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=K+Mil%C3%AD%C4%8Dovu#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Ke+Kr%C4%8Di#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Krosensk%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Lou%C4%8Dimsk%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Molitorovsk%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Na+Laurov%C3%A9#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Na+%C4%8Cervence#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Nezamyslova+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Petrsk%C3%A1+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Pod+vod%C3%A1renskou+v%C4%9B%C5%BE%C3%AD+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Radho%C5%A1%C5%A5sk%C3%A1+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Sladovnick%C3%A1+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Tachlovick%C3%A1#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=U+klubovny+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=U+tr%C5%BEnice+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=V+pr%C5%AFhledu#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Vr%C5%A1ovka+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=Zvona%C5%99sk%C3%A1+%28Prague%29#mw-subcategories',
				'https://commons.wikimedia.org/w/index.php?title=Category:Streets_in_Prague_by_name&subcatfrom=%C5%A0t%C3%ADbrova#mw-subcategories']
		return arr
StreetGetter()

# https://www.sreality.cz/ru/search/to-rent/apartments/praha?disposition=1%2Bkt,1%2B1,2%2B1,2%2Bkt,3%2Bkt,3%2B1&		status=very-good-condition,good-condition
# https://www.sreality.cz/ru/search/to-rent/apartments/praha?disposition=1%2Bkt,1%2B1,2%2Bkt,2%2B1,3%2Bkt,3%2B1&		status=very-good-condition,good-condition
# https://www.sreality.cz/ru/search/to-rent/apartments/praha?disposition=1%2Bkt,1%2B1,2%2B1,2%2Bkt,3%2Bkt,3%2B1&	status=very-good-condition,good-condition&page=2
# https://www.sreality.cz/ru/search/to-rent/apartments/praha?disposition=1%2Bkt,1%2B1,2%2Bkt,2%2B1,3%2Bkt,3%2B1&furnished=fully&status=very-good-condition,good-condition
from seleniumwire import webdriver
import requests
from bs4 import BeautifulSoup as bs
url = 'https://www.sreality.cz/ru/search/to-rent/apartments/praha?disposition=1a%2Bkt,2%2Bkt,1%2B1,2%2B1,3%2Bkt,3%2B1&furnished=fully&status=very-good-condition,good-condition&page={}'
for page in range(1,48):
	cur_url = url.format(page)
	driver = webdriver.Chrome(executable_path = 'C:/Users/Tom/Downloads/chromedriver_win32/chromedriver.exe')
	driver.set_window_size(1920, 1080)
	# divs = soup.find_all("div", class_ = "property ng-scope")
	# for div in divs:
	# 	cur_home = div.find("a")
	# 	print(cur_home)
	print(mdiv)
	break
	# find all property id ="ng-scope"
	# open that page
	# norm-price ng-binding - cut 
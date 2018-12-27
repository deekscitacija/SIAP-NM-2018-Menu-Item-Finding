from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=option)

browser.get('https://www.donesi.com/')

html = browser.page_source

soup = BeautifulSoup(html, "html.parser")

countries = soup.find_all("div", {'class' : 'card'})

cities = [ {'cityName' :city.h4.text, 'country' : city.h4.a['data-gtm-country'], 'path' : city.h4.a['href']} for country in countries for city in country.div.ul.findChildren('li')]

browser.find_element_by_xpath('//a[@href="'+cities[0]['path']+'"]').click()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import scraper

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=option)

def goToCityPages():
    browser.get('https://www.donesi.com/')

    html = browser.page_source
    cities = scraper.getCityLinks(html)

    #for city in cities:
        #browser.find_element_by_xpath('//a[@href="'+city+'"]').click()

    browser.find_element_by_xpath('//a[@href="'+cities[0]+'"]').click()
    


    




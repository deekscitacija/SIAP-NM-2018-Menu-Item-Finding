from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
import scraper

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=option)

browser.get("https://www.donesi.com/")

html = browser.page_source
cities = scraper.getCities(html)

#for city in cities:
    #browser.find_element_by_xpath('//a[@href="'+city+'"]').click()
    #browser.get(city)

currentPage = cities[0]
restaurants = []

while(currentPage):
    browser.get(currentPage)
    html = browser.page_source

    retVal = scraper.getRestaurantsForCity(html)
    restaurants.extend(retVal["restaurants"])
    currentPage = retVal["nextPage"]

x = 0
reviews = []
for restaurantData in restaurants:
    x+=1
    if x == 5:
        break
    browser.get(restaurantData["link"])
    html = browser.page_source
    scraper.getMenuItemsForRestaurant(restaurantData,html)

    #currentPage = restaurantData["link"]+"#tab-reviews"
    #browser.get(currentPage)
    #html = browser.page_source
    #currentPage = scraper.getExpandedPageURL(html, "a", "Prikaži sve...")["href"]

    #while(currentPage):
        #browser.get(currentPage)
        #html = browser.page_source
        #retVal = scraper.getRecensionData(restaurantData, html)
        #reviews.extend(retVal["reviews"])
        #currentPage = retVal["nextPage"]
    



    




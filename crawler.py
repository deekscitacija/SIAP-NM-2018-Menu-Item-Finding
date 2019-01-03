from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
import scraper

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

srb = ["Beograd", "Novi Sad", "Nis", "Subotica", "Pancevo", "Zrenjanin", "Kragujevac", "Krusevac", "Kraljevo", "Cacak"]

restaurantsNum = 3000

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=option)

def getRestaurantUrl(city, id):
    return "http://www.donesi.com/" + city.lower().replace(" ", "") + "/lat/review.php?objectID=" + str(id)

cityIndex = 0
for city in srb:
    if cityIndex == 2:
        break

    restaurantId = 735
    while(restaurantId!=739):
        currentRestaurantUrl = getRestaurantUrl(city, restaurantId)
        browser.get(currentRestaurantUrl)
        if currentRestaurantUrl == browser.current_url:

            html = browser.page_source

            if(scraper.hasResults(html)):
                if(scraper.hasRevews(html)):
                    currentRestaurantUrl = scraper.getReviewData(restaurantId, html, db)
                    while(currentRestaurantUrl):
                        browser.get(currentRestaurantUrl)
                        html = browser.page_source
                        currentRestaurantUrl = scraper.getReviewData(restaurantId, html, db)
                    
                    restaurantData = scraper.getRestaurantData(html)
                    browser.get(restaurantData["restaurantLink"])
                    html = browser.page_source

                    scraper.getMenuItemsForRestaurant(restaurantId, restaurantData["restaurantName"], city, html, db)

        restaurantId = restaurantId + 1

    cityIndex = cityIndex+1   
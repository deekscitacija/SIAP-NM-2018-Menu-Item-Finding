from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
import scraper

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

srb =  {"name" : "Srbija", "cities" : ["Beograd", "Novi Sad", "Nis", "Subotica", "Pancevo", "Zrenjanin", "Kragujevac", "Krusevac", "Kraljevo", "Cacak"]}

restaurantsNum = 2101

option = webdriver.ChromeOptions()
option.add_argument("--incognito")

browser = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=option)

def getRestaurantUrl(city, id):
    return "http://www.donesi.com/" + city.lower().replace(" ", "") + "/lat/review.php?objectID=" + str(id)

def getRestaurantsForCountry(country):
    for city in country["cities"]:
        getRestaurantsForCity(country, city)

def getRestaurantsForCity(country, city):
    for restaurantId in range(1, restaurantsNum):
        getRestaurantData(country, city, restaurantId)

def getRestaurantData(country, city, restaurantId):
    currentRestaurantUrl = getRestaurantUrl(city, restaurantId)
    browser.get(currentRestaurantUrl)
    if currentRestaurantUrl == browser.current_url:
        html = browser.page_source
        if(scraper.hasResults(html)):
            if(scraper.hasRevews(html)):
                restaurantData = scraper.getRestaurantData(html)
                restaurantLink = restaurantData["restaurantLink"]
                currentRestaurantUrl = scraper.getReviewData(restaurantLink, html, db)
                while(currentRestaurantUrl):
                    browser.get(currentRestaurantUrl)
                    html = browser.page_source
                    currentRestaurantUrl = scraper.getReviewData(restaurantLink, html, db)

                browser.get(restaurantLink)
                html = browser.page_source

                scraper.getMenuItemsForRestaurant(restaurantLink, restaurantData["restaurantName"], country["name"], city, html, db)

if __name__ == "__main__":
        getRestaurantsForCountry(srb)

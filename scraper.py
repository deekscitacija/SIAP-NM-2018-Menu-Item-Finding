from bs4 import BeautifulSoup

def getCities(html):
    soup = BeautifulSoup(html, "html.parser")

    countryNames = ["Serbia"]
    countries = soup.find_all("div", {"class" : "card"})
    cities = ["https:"+city["href"] for country in countries for city in country.find_all("a") if city["data-gtm-country"] in countryNames]

    return cities

def getRestaurantsForCity(html):
    soup = BeautifulSoup(html, "html.parser")

    restaurantsDiv = soup.find("div", {"class" : "tab-content"})
    restaurants = [restaurant.div.div.find("div", {"class" : None}).div.find("div", {"class" : "span2 text-center"}).a["href"] for restaurant in restaurantsDiv.find("ul").findChildren("li")]

    nextPage = soup.find("a", {"class" : "jscroll-next"}) 
    print(restaurants)
    return {"restaurants" : restaurants, "nextPage" : nextPage["href"] if nextPage is not None else None}






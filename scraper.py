from bs4 import BeautifulSoup

def getCities(html):
    soup = BeautifulSoup(html, "html.parser")

    countryNames = ["Serbia"]
    countries = soup.find_all("div", {"class" : "card"})
    cities = ["https:"+city["href"]+"lat/" for country in countries for city in country.find_all("a") if city["data-gtm-country"] in countryNames]

    return cities

def getRestaurantsForCity(html):
    soup = BeautifulSoup(html, "html.parser")

    restaurantsDiv = soup.find("div", {"class" : "tab-content"})
    restaurants = []
    for restaurant in restaurantsDiv.find("ul").findChildren("li"):
        tempRestaurant = restaurant.div.div.find("div", {"class" : None}).div.find("div", {"class" : "span2 text-center"}).a
        restaurants.append({"link" : tempRestaurant["href"], "id" : tempRestaurant["data-oid"]})

    nextPage = soup.find("a", {"class" : "jscroll-next"}) 
  
    return {"restaurants" : restaurants, "nextPage" : nextPage["href"] if nextPage is not None else None}

def getMenuItemsForRestaurant(restaurantData, html):
    soup = BeautifulSoup(html, "html.parser")
    
    menuItemCategories = soup.find_all("section", id=lambda x: x and x.startswith('scroll'))
    menuItems = []
    for menuItemCategory in menuItemCategories:
        for menuItem in menuItemCategory.find("div", {"class" : "masonery "}).find_all("div", {"class" : "card food"}):
            menuItemName = menuItem.find("div", {"class" : "card-heading image"}).find("div", {"class" : "card-heading-header"}).find("h3", {"itemprop" : "name"})
            menuItems.append(menuItemName.a.text) if menuItemName.a is not None else menuItems.append(menuItemName.text)

def getRecensionData(restaurantData, html):
    soup = BeautifulSoup(html, "html.parser")

    reviewContainers = soup.find_all("div", {"class" : "card review reviewcontainer"})
    nextPage = soup.find("a", {"id" : "nav_next_page"})
    reviews = []

    for reviewContainer in reviewContainers:

        title = reviewContainer.find("div", {"class" : "row-fluid"}).find("div", {"class" : "span10"}).find("div", {"class" : "reviewtitle"}).a.text
        reviewBody = reviewContainer.find("span", {"itemprop" : "reviewBody"}).text
        reviewDate = reviewContainer.find("meta", {"itemprop" : "datePublished"})["content"]
        userRankContainer = reviewContainer.find("span", {"class" : "ulev"})
        reviewUserRank = userRankContainer.text if userRankContainer is not None else None

        ratings = []
        ratingInfos = reviewContainer.find_all("td", {"class" : "rate-cell-5"})
        for ratingInfo in ratingInfos:
            rating = { ratingInfo.small.text : ratingInfo.b.text }
            ratings.append(rating)

        review = {"restaurantId" : restaurantData["id"], "title" : title, "reviewBody" : reviewBody, "date" : reviewDate, "userRank" : reviewUserRank, "ratings" : ratings}
        reviews.append(review)

    return {"reviews" : reviews, "nextPage" : nextPage["href"] if nextPage is not None else None}

def getExpandedPageURL(html, tagName, param):
    soup = BeautifulSoup(html, "html.parser")
    theTag = soup.find(lambda tag:tag.name==tagName and param in tag.text)
    return theTag
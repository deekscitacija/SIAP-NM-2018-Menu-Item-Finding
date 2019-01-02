from bs4 import BeautifulSoup

def hasResults(html):
    return "Nije dostupno!" not in html

def hasRevews(html):
    return "Ne postoji nijedan utisak o ovome restoranu. Budite prvi koji će ga oceniti!" not in html

def getReviewData(restaurantId, html):
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

        review = {"restaurantId" : restaurantId, "title" : title, "reviewBody" : reviewBody, "date" : reviewDate, "userRank" : reviewUserRank, "ratings" : ratings}
        reviews.append(review)

    return nextPage["href"] if nextPage is not None else None

def getMenuItemsForRestaurant(restaurantId, restaurantName, restaurantCity, html):
    soup = BeautifulSoup(html, "html.parser")
    
    menuItemCategories = soup.find_all("section", id=lambda x: x and x.startswith("scroll"))
    menuItems = []
    for menuItemCategory in menuItemCategories:
        for menuItem in menuItemCategory.find("div", {"class" : "masonery "}).find_all("div", {"class" : "card food"}):
            menuItemName = menuItem.find("div", {"class" : "card-heading image"}).find("div", {"class" : "card-heading-header"}).find("h3", {"itemprop" : "name"})
            menuItems.append(menuItemName.a.text) if menuItemName.a is not None else menuItems.append(menuItemName.text)
            
    print(menuItems)

def getRestaurantData(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("a", string=lambda x : x and x.startswith("Jelovnik"))
    
    restaurantData = {"restaurantName" : None, "restaurantLink" : None}

    if tag is not None:
        restaurantData["restaurantName"] = tag.text.strip()[9:]
        restaurantData["restaurantLink"] = tag["href"]

    return restaurantData

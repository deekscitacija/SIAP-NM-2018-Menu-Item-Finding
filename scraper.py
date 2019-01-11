from bs4 import BeautifulSoup
import datetime
import alphabetConverter as ac

def hasResults(html):
    return "Nije dostupno!" not in html

def hasRevews(html):
    return "Ne postoji nijedan utisak o ovome restoranu. Budite prvi koji će ga oceniti!" not in html

def getReviewData(restaurantLink, html, db):
    soup = BeautifulSoup(html, "html.parser")

    reviewContainers = soup.find_all("div", {"class" : lambda x : x and x.startswith("card review reviewcontainer")})
    nextPage = soup.find("a", {"id" : "nav_next_page"})
    
    for reviewContainer in reviewContainers:

        title = reviewContainer.find("div", {"class" : "row-fluid"}).find("div", {"class" : "span10"}).find("div", {"class" : "reviewtitle"}).a.text.strip()
        reviewBody = reviewContainer.find("span", {"itemprop" : "reviewBody"}).text.strip()
        reviewDateString = reviewContainer.find("meta", {"itemprop" : "datePublished"})["content"].strip()
        reviewUserName = reviewContainer.find("a", {"itemprop" : "author"}).text.strip()
        userRankContainer = reviewContainer.find("span", {"class" : "ulev"})
        reviewUserRank = userRankContainer.text.strip() if userRankContainer is not None else None

        ratings = []
        ratingInfos = reviewContainer.find_all("td", {"class" : "rate-cell-5"})
        for ratingInfo in ratingInfos:

            rating = {convertRating(ratingInfo.small.text) : int(ratingInfo.b.text.strip())}
            ratings.append(rating)

        review = {"restaurantLink" : restaurantLink, "title" : ac.cyrilicToLatin(title), "reviewBody" : ac.cyrilicToLatin(reviewBody), "date" : convertDate(reviewDateString), "userName" : reviewUserName, "userRank" : reviewUserRank, "ratings" : ratings}
        db['RestaurantReviews'].insert(review)

    return nextPage["href"] if nextPage is not None else None

def getMenuItemsForRestaurant(restaurantLink, restaurantName, restaurantCountry, restaurantCity, html, db):
    soup = BeautifulSoup(html, "html.parser")
    
    menuItemCategories = soup.find_all("section", id=lambda x: x and x.startswith("scroll"))
    menuItems = []
    for menuItemCategory in menuItemCategories:
        for menuItemContainer in menuItemCategory.find("div", lambda x : x and x.startswith("masonery")).find_all("div", {"class" : "card food"}):
            menuItemDataContainer = menuItemContainer.find("div", {"class" : "card-heading image"}).find("div", {"class" : "card-heading-header"})
            menuItemName = menuItemDataContainer.find("h3", {"itemprop" : "name"})

            menuItem = {}
            menuItem["name"] = ac.cyrilicToLatin(menuItemName.a.text.strip()) if menuItemName.a is not None else ac.cyrilicToLatin(menuItemName.text.strip())            
            menuItem["description"] = ac.cyrilicToLatin(menuItemDataContainer.find("span", {"itemprop" : "description"}).text.strip())
            menuItems.append(menuItem)

    restaurant = {"restaurantLink" : restaurantLink, "restaurantName" : restaurantName, "restaurantCountry" : restaurantCountry, "restaurantCity" : restaurantCity, "menuItems" : menuItems}
    db["Restaurants"].insert(restaurant)

def getRestaurantData(html):
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("a", string=lambda x : x and x.startswith("Jelovnik"))
    
    restaurantData = {"restaurantName" : None, "restaurantLink" : None}

    if tag is not None:
        restaurantData["restaurantName"] = tag.text.strip()[9:]
        restaurantData["restaurantLink"] = tag["href"]

    return restaurantData

def convertRating(value):
    return {
        'Kvalitet hrane': 'food_quality',
        'Izbor hrane': 'food_choice',
        'Cene': 'price',
        'Usluga': 'service'
    }[value]

def convertDate(dateString):
    format = "%Y-%m-%d"
    return datetime.datetime.strptime(dateString,format)

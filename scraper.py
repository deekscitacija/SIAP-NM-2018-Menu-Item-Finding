from bs4 import BeautifulSoup

def hasResults(html):
    return "Nije dostupno!" not in html

def hasRevews(html):
    return "Ne postoji nijedan utisak o ovome restoranu. Budite prvi koji će ga oceniti!" not in html

def getReviewData(restaurantId, html, db):
    soup = BeautifulSoup(html, "html.parser")

    reviewContainers = soup.find_all("div", {"class" : "card review reviewcontainer"})
    nextPage = soup.find("a", {"id" : "nav_next_page"})

    for reviewContainer in reviewContainers:

        title = reviewContainer.find("div", {"class" : "row-fluid"}).find("div", {"class" : "span10"}).find("div", {"class" : "reviewtitle"}).a.text
        reviewBody = reviewContainer.find("span", {"itemprop" : "reviewBody"}).text
        reviewDate = reviewContainer.find("meta", {"itemprop" : "datePublished"})["content"]
        userRankContainer = reviewContainer.find("span", {"class" : "ulev"})
        reviewUserRank = userRankContainer.text if userRankContainer is not None else None

        ratings = []
        ratingInfos = reviewContainer.find_all("td", {"class" : "rate-cell-5"})
        for ratingInfo in ratingInfos:

            rating = { convertRating(ratingInfo.small.text) : ratingInfo.b.text }
            ratings.append(rating)

        review = {"restaurantId" : restaurantId, "title" : cyrilicToLatin(title), "reviewBody" : cyrilicToLatin(reviewBody), "date" : reviewDate, "userRank" : reviewUserRank, "ratings" : ratings}
        #db['Reviews'].insert(review)

    return nextPage["href"] if nextPage is not None else None

def getMenuItemsForRestaurant(restaurantId, restaurantName, restaurantCity, html, db):
    soup = BeautifulSoup(html, "html.parser")
    
    restaurant = db["Restaurants"].find_one({"restaurantId" : restaurantId})
    print(restaurant)
    
    menuItemCategories = soup.find_all("section", id=lambda x: x and x.startswith("scroll"))
    menuItems = []
    for menuItemCategory in menuItemCategories:
        for menuItemContainer in menuItemCategory.find("div", {"class" : "masonery "}).find_all("div", {"class" : "card food"}):
            menuItemDataContainer = menuItemContainer.find("div", {"class" : "card-heading image"}).find("div", {"class" : "card-heading-header"})
            menuItemName = menuItemDataContainer.find("h3", {"itemprop" : "name"})

            menuItem = {}
            menuItem["name"] = menuItemName.a.text if menuItemName.a is not None else cyrilicToLatin(menuItemName.text)            
            menuItem["description"] = cyrilicToLatin(menuItemDataContainer.find("span", {"itemprop" : "description"}).text)

            menuItems.append(menuItem)

    db["Restaurants"].update_one({"_id" : restaurant["_id"]}, {"$set" : {"menuItems" : menuItems}})

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
        'Kvalitet hrane': 'kvalitet_hrane',
        'Izbor hrane': 'izbor_hrane',
        'Cene': 'cene',
        'Usluga': 'usluga'
    }[value]

def cyrilicToLatin(value):

    if any(c in "абвгдђежзијклљмнљопрстћуфхцчџшАБВГДЂЕЖЗИЈКЛЉМНЊОПРСТЋУФХЦЧЏШ" for c in value):
        print('uslooooo')
        retVal = value
        # Mala slova
        retVal = retVal.replace('а', 'a')
        retVal = retVal.replace('б', 'b')
        retVal = retVal.replace('в', 'v')
        retVal = retVal.replace('г', 'g')
        retVal = retVal.replace('д', 'd')
        retVal = retVal.replace('ђ', 'đ')
        retVal = retVal.replace('е', 'e')
        retVal = retVal.replace('ж', 'ž')
        retVal = retVal.replace('з', 'z')
        retVal = retVal.replace('и', 'i')
        retVal = retVal.replace('ј', 'j')
        retVal = retVal.replace('к', 'k')
        retVal = retVal.replace('л', 'l')
        retVal = retVal.replace('љ', 'lj')
        retVal = retVal.replace('м', 'm')
        retVal = retVal.replace('н', 'n')
        retVal = retVal.replace('њ', 'nj')
        retVal = retVal.replace('о', 'o')
        retVal = retVal.replace('п', 'p')
        retVal = retVal.replace('р', 'r')
        retVal = retVal.replace('с', 's')
        retVal = retVal.replace('т', 't')
        retVal = retVal.replace('ћ', 'ć')
        retVal = retVal.replace('у', 'u')
        retVal = retVal.replace('ф', 'f')
        retVal = retVal.replace('х', 'h')
        retVal = retVal.replace('ц', 'c')
        retVal = retVal.replace('ч', 'č')
        retVal = retVal.replace('џ', 'dž')
        retVal = retVal.replace('ш', 'š')
        # Velika slova
        retVal = retVal.replace('А', 'A')
        retVal = retVal.replace('Б', 'B')
        retVal = retVal.replace('В', 'V')
        retVal = retVal.replace('Г', 'G')
        retVal = retVal.replace('Д', 'D')
        retVal = retVal.replace('Ђ', 'Đ')
        retVal = retVal.replace('Е', 'E')
        retVal = retVal.replace('Ж', 'Ž')
        retVal = retVal.replace('З', 'Z')
        retVal = retVal.replace('И', 'I')
        retVal = retVal.replace('Ј', 'J')
        retVal = retVal.replace('К', 'K')
        retVal = retVal.replace('Л', 'L')
        retVal = retVal.replace('Љ', 'LJ')
        retVal = retVal.replace('М', 'M')
        retVal = retVal.replace('Н', 'N')
        retVal = retVal.replace('Њ', 'NJ')
        retVal = retVal.replace('О', 'O')
        retVal = retVal.replace('П', 'P')
        retVal = retVal.replace('Р', 'R')
        retVal = retVal.replace('С', 'S')
        retVal = retVal.replace('Т', 'T')
        retVal = retVal.replace('Ћ', 'Ć')
        retVal = retVal.replace('У', 'U')
        retVal = retVal.replace('Ф', 'G')
        retVal = retVal.replace('Х', 'H')
        retVal = retVal.replace('Ц', 'C')
        retVal = retVal.replace('Ч', 'Č')
        retVal = retVal.replace('Џ', 'DŽ')
        retVal = retVal.replace('Ш', 'Š')
        return retVal
    
    return value

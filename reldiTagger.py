import json
from reldi.parser import Parser
from pymongo import MongoClient
from unidecode import unidecode

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def startProgram():
    startId = input("Unesite filtriranu recenziju od koje cete da zapocnete tagovanje:")
    reviewNum = input("Unesite za koliko filtriranih recenzija cete da odradite tagovanje:")
    try:
        startPoint = int(startId)
        endPoint = int(reviewNum)
        tagReviews(startPoint,endPoint)
    except ValueError:
        print("Unos neuspesan!")

def tagReviews(startPoint, endPoint):

    p = Parser('sr')
    p.authorize('igor_trpovski','SifrazaIgoraSIAPreldi!2018')

    reviewCount = 0
    while(reviewCount < endPoint):
        reviewCount = reviewCount+1
        reviews = db['FilteredRestaurantReviews'].find()[startPoint:startPoint+1]

        for review in reviews:
            reviewObject = {"restaurantLink" : review["restaurantLink"], "title" : review["title"], "reviewBody" : review["reviewBody"], "date" : review["date"], "userName" : review["userName"], "userRank" : review["userRank"], "ratings" : review["ratings"]}
            reldiObject = json.loads(p.tagLemmatiseParse(getReviewContent(reviewObject)))
            tokens = reldiObject["tokens"]
            namedEntities = []
            tokenNum = 0
            for token in tokens["token"]:
                namedEntity = {"ID" : "nt_"+str(tokenNum), "tokenIDs" : token["ID"], "value" : "O"}
                namedEntities.append(namedEntity)
                tokenNum+=1

            namedEntityObject = {"namedEntities" : {"entity" : namedEntities}}
            filteredAndTaggedRestaurantReview = reviewObject.copy()
            filteredAndTaggedRestaurantReview.update(reldiObject)
            filteredAndTaggedRestaurantReview.update(namedEntityObject)
            db["FilteredAndTaggedRestaurantReviews"].insert_one(filteredAndTaggedRestaurantReview)
            
            startPoint = startPoint+1     

def getReviewContent(review):

    reviewContent = ""
    reviewTitle = review["title"]
    reviewBody = review["reviewBody"]

    if reviewTitle!="" and reviewBody!="":
        reviewContent = reviewTitle+"\n"+reviewBody
    elif reviewTitle=="":
        reviewContent = reviewBody
    elif reviewBody=="":
        reviewContent = reviewTitle
    
    retVal = unidecode(reviewContent)

    return retVal

if __name__ == "__main__":
    startProgram()

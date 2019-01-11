from pymongo import MongoClient
import alphabetConverter as ac

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def filterReviews(startPoint):
    loop = True
    while(loop):
        reviews = db['RestaurantReviews'].find()[startPoint:startPoint+1]
        for review in reviews:
            reviewTitle = review["title"]
            reviewBody = review["reviewBody"]
            print("Naslov:")
            print("\t"+reviewTitle)
            print("Sadrzaj:")
            print("\t"+reviewBody)
            
            userInput = input("Da li se u recenziji nalazi stavka menija? (Y/N):")
            if userInput in 'yY':
                filteredReview = {"restaurantLink" : review["restaurantLink"], "title" : ac.serbianLatinToLatin(reviewTitle), "reviewBody" : ac.serbianLatinToLatin(reviewBody), "date" : review["date"], "userName" : review["userName"], "userRank" : review["userRank"], "ratings" : review["ratings"]}
                db['FilteredRestaurantReviews'].insert(filteredReview)
            elif userInput not in 'nN':
                loop = False
                break

            print("\nObradili ste dokument sa rednim brojem: "+str(startPoint)+" i sa identifikatorom: "+str(review["_id"]))
            print("________________________________________________________________________________________________________\n")
        
        startPoint = startPoint+1

def startProgram():
    userInput = input("Unesite recenziju od koje cete da zapocnete filtriranje:")
    try:
        startPoint = int(userInput)
        filterReviews(startPoint)
    except ValueError:
        print("Niste uneli broj")

if __name__ == "__main__":
    startProgram()


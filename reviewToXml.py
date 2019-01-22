from pymongo import MongoClient
import xml.etree.cElementTree as xmlET

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def startProgram():
    startId = input("Unesite recenziju od koje cete da zapocnete generisanje Xml-a:")
    reviewNum = input("Unesite za koliko recenzija ce se vrsiti generisanje Xml-a:")
    try:
        startPoint = int(startId)
        endPoint = int(reviewNum)
        exportXml(startPoint, endPoint)
    except ValueError:
        print("Unos neuspesan!")

def exportXml(startPoint, endPoint):

    reviewCount = 0
    while(reviewCount < endPoint):
        reviewCount = reviewCount+1
        reviews = db['RestaurantReviews'].find()[startPoint:startPoint+1]

        for review in reviews:
            root = xmlET.Element("ReviewsTask")
            reviewText = xmlET.SubElement(root, "TEXT")
            reviewText.append(xmlET.Comment(' --><![CDATA[' + getReviewContent(review).replace(']]>', ']]]]><![CDATA[>') + ']]><!-- '))
            tags = xmlET.SubElement(root, "TAGS").text = " "

            tree = xmlET.ElementTree(root)
            tree.write("reviewsXml/"+str(review["_id"])+".xml", encoding='UTF-8', xml_declaration=True)

            startPoint = startPoint+1

def getReviewContent(review):
    return review["title"]+"\n"+review["reviewBody"].replace('\n', '').replace('\t', '')
        

if __name__ == "__main__":
    startProgram()
from pymongo import MongoClient
import tkinter as tk
from tkinter import filedialog
import random, os

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def startProgram():
    startId = input("Unesite recenziju od koje cete da zapocnete generisanje datoteke: ")
    reviewNum = input("Unesite za koliko recenzija ce se vrsiti generisanje datoteke: ")
    trainNum = input("Unesite procenat recenzija koji ce biti u trening skupu: ")
    fileName = input("Izaberite naziv datoteke: ")
    try:
        startPoint = int(startId)
        endPoint = int(reviewNum)
        trainPercent = float(trainNum)
        if trainPercent <= 0 or trainPercent >=1:
            raise ValueError()
        train = random.sample(range(startPoint,endPoint), int(trainPercent*endPoint))
        root = tk.Tk()
        root.withdraw()
        folderPath = filedialog.askdirectory()
        exportToTxt(startPoint, endPoint, folderPath, fileName, train)
        
    except ValueError:
        print("Unos neuspesan!")

def exportToTxt(startPoint, endPoint, folderPath, fileName, train):
    
    with open(folderPath+os.path.sep+fileName+"Train", "a", encoding="utf-8") as fileTrain, open(folderPath+os.path.sep+fileName+"Test", "a", encoding="utf-8") as fileTest:
    
        reviewCount = 0
        while(reviewCount < endPoint):
            print("Izvrsava se: "+reviewCount)
            if reviewCount in train:
                f = fileTrain
            else:
                f = fileTest

            reviewCount = reviewCount+1
            reviews = db['FilteredAndTaggedRestaurantReviews'].find()[startPoint:startPoint+1]

            if len(reviews) == 0:
                break

            for review in reviews:
                reviewId = str(review["_id"])
                propertyValues = list(zip(review['tokens']['token'],review['lemmas']['lemma'],review['POStags']['tag'],review['namedEntities']['entity']))
                propertyIdx = -1

                for sentence in review['sentences']['sentence']:
                    sentenceId = sentence['ID']
                    tokenIds = sentence['tokenIDs'].split(' ')
                
                    for tokenId in tokenIds:
                        propertyIdx = propertyIdx+1
                        tempTokenId = propertyValues[propertyIdx][1]['tokenIDs']
                        tempText = propertyValues[propertyIdx][0]['text']
                        tempPOS = propertyValues[propertyIdx][2]['text']
                        tempLemma = propertyValues[propertyIdx][1]['text']
                        tempNer = propertyValues[propertyIdx][3]['value']

                        if tempTokenId == tokenId:
                            f.write(reviewId+"~"+sentenceId+"~"+tokenId+"\t")
                            f.write(tempText+"\t")
                            f.write(tempPOS+"\t")
                            f.write(tempLemma+"\t")
                            f.write(str(tempText.isdigit())+"\t")
                            f.write(str(tempPOS == 'Z')+"\t")
                            f.write(str(tempText.isupper())+"\t")
                            f.write(str(tempText[0].isupper() and tempText[1:].islower())+"\t")
                            f.write(str(tempTokenId == tokenIds[-1])+"\t")
                            f.write(tempNer+"\t")
                            f.write("\n")
                    f.write("\n")  
                startPoint = startPoint+1

if __name__ == "__main__":
    startProgram()
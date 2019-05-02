from pymongo import MongoClient
from bson.objectid import ObjectId
import tkinter as tk
from tkinter import filedialog
from copy import deepcopy
import os, csv, json

class MenuItem(object):
    startOffset = -1
    endOffset = -1
    items = []
    text = ""

    def __init__(self, startOffset, endOffset, items, text):
        self.startOffset = startOffset
        self.endOffset = endOffset
        self.items = items
        self.text = text

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']
dbReviews = db['FilteredAndTaggedRestaurantReviews']

def parseCrfFile(filePath):

    with open(filePath, "r", encoding="utf-8") as crfFile:

        reader = csv.reader(crfFile, delimiter = '\t')

        dbReview = {'_id' : None}                                       # Holds review object from database                      
        offsetPosition = 0                                              # Current position in review 
        lastTag = 'O'                                                   # Tag of previous token
        menuItems = []                                                  # Temp array of meny items in current review
        menuItem = MenuItem(-1, -1, [], "")                             # Temp menu item object 

        for fileLine in reader:

            if len(fileLine) > 0:
                reviewId = fileLine[0].split('~')[0]
        
                if reviewId != str(dbReview['_id']):                    #Get next review from DB and save current to JSON file
                    
                    if dbReview['_id'] != None:
                        exportReview(filePath, dbReview, menuItems)
                    
                    offsetPosition = 0
                    dbReview = dbReviews.find_one(ObjectId(reviewId))
                    menuItems = []

                tokenNum = int(fileLine[0].split('~')[2][2:])           # Position in tags array in review object
                tokenInfo = dbReview['tokens']['token'][tokenNum]
                tokenLen = int(tokenInfo['end']) - int(tokenInfo['start'])
                reviewOriginalText = dbReview['text']
                foundTag = fileLine[13]                                 # BILOU tag labeled by CRF 

                offsetPosition = calculateOffset(offsetPosition, tokenInfo, tokenLen, reviewOriginalText)
                retVal = bindNewTag(menuItem, foundTag, lastTag, offsetPosition, tokenLen)
                
                if retVal == 'END':
                    menuItem.text = reviewOriginalText[menuItem.startOffset:menuItem.endOffset]
                    menuItems.append(deepcopy(menuItem)) 
                if retVal == 'FAIL' or retVal == 'END':
                    foundTag = 'O'
                    menuItem.items = []

                lastTag = foundTag
        
        exportReview(filePath, dbReview, menuItems)

        
def exportReview(filePath, dbReview, menuItems):
    with open(os.path.dirname(filePath)+os.path.sep+str(dbReview['_id'])+".json", "w", encoding="utf-8") as outJSON:
            jsonData = buildReviewObject(str(dbReview['_id']), dbReview['restaurantLink'], menuItems)
            json.dump(jsonData, outJSON)

def buildReviewObject(reviewId, restaurantLink, menuItems):

    menuItemObjects = []
    for menuItem in menuItems:
        menuItemObjects.append({'text' : menuItem.text})

    return {'id' : reviewId, 'restaurantLink' : restaurantLink, 'menuItems' : menuItemObjects}

def calculateOffset(offsetPosition, tokenInfo, tokenLen, reviewOriginalText):
    beginingIdx = reviewOriginalText.find(tokenInfo['text'], offsetPosition)
    return beginingIdx+tokenLen

def bindNewTag(menuItem, labeledTag, lastTag, offsetPosition, tokenLen):
    
    if labeledTag == 'U-FOOD' :
        menuItem.items = [ labeledTag ]
        menuItem.startOffset = offsetPosition-tokenLen
        menuItem.endOffset = offsetPosition+1
        return 'END'

    elif labeledTag == 'B-FOOD' and (lastTag == 'O' or lastTag == 'U-FOOD'):
        menuItem.items = [ labeledTag ]
        menuItem.startOffset = offsetPosition-tokenLen
        return 'CONTINUE'

    elif labeledTag == 'I-FOOD' and (lastTag == 'B-FOOD' or lastTag == 'I-FOOD'):
        menuItem.items.append(labeledTag)
        return 'CONTINUE'

    elif labeledTag == 'L-FOOD' and (lastTag == 'B-FOOD' or lastTag == 'I-FOOD'):
        menuItem.items.append(labeledTag)
        menuItem.endOffset = offsetPosition+1
        return 'END'

    else:
        return 'FAIL'

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filePath = filedialog.askopenfile()
    parseCrfFile(filePath.name)

if __name__ == "__main__":
    startProgram()


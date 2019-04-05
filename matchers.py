from pymongo import MongoClient
from bson.objectid import ObjectId
import tkinter as tk
from tkinter import filedialog
import alphabetConverter as ac
import os, csv, json

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']
dbRestaurants = db['Restaurants']

filePaths = []

def processFiles():
    dbRestaurant = {'restaurantLink' : None}

    for filePath in filePaths:
        with open(filePath, "r", encoding="utf-8") as reviewJsonFile:
            reviewObject = json.load(reviewJsonFile)

            if reviewObject['restaurantLink'] != str(dbRestaurant['restaurantLink']):
                dbRestaurant = dbRestaurants.find_one({'restaurantLink' : reviewObject['restaurantLink']}) 
                
                for menuItem in dbRestaurant['menuItems']:
                    menuItem['name'] = ac.removeSpecialTags(ac.serbianLatinToLatin(menuItem['name']))

def readAllFiles(folderPath):
    allFiles = os.listdir(folderPath)

    for tempItem in allFiles:
        fullFilePath = folderPath+os.path.sep+tempItem
        
        if os.path.isdir(fullFilePath):
            readAllFiles(fullFilePath)
        else:
            if fullFilePath.endswith('_match.json'):
                filePaths.append(fullFilePath)

def startProgram():
    folderPath = filedialog.askdirectory()
    readAllFiles(folderPath)
    if(len(filePaths) > 0):
        processFiles()

if __name__ == "__main__":
    startProgram()
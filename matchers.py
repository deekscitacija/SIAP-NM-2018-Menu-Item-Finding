from pymongo import MongoClient
from bson.objectid import ObjectId
from tkinter import filedialog
from pyjarowinkler import distance
import tkinter as tk
import alphabetConverter as ac
import serbianStemmer as stemmer
import os, csv, json

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']
dbRestaurants = db['Restaurants']
filePaths = []

def processFiles(folderPath, filePaths):
    dbRestaurant = {'restaurantLink' : None}

    with open(folderPath+os.path.sep+"outputMatchers.txt", "w", encoding="utf-8") as outputFile:
        tsv_writer = csv.writer(outputFile, delimiter='\t', lineterminator='\n')

        for filePath in filePaths:
            with open(filePath, "r", encoding="utf-8") as reviewJsonFile:
                reviewObject = json.load(reviewJsonFile)

                if reviewObject['restaurantLink'] != str(dbRestaurant['restaurantLink']):
                    dbRestaurant = dbRestaurants.find_one({'restaurantLink' : reviewObject['restaurantLink']}) 
                    
                    for menuItem in dbRestaurant['menuItems']:
                        menuItem['name'] = ac.removeSpecialTags(ac.serbianLatinToLatin(menuItem['name']))
                
                for foodItem in reviewObject['menuItems']:
                    exactMatchStr = exactMatch(foodItem['text'], dbRestaurant['menuItems'])
                    substringMatchStr = substringMatch(foodItem['text'], dbRestaurant['menuItems'])
                    fuzzyMatchStr = fuzzyMatch(foodItem['text'], dbRestaurant['menuItems'])
                    partialMatchStr = partialMatch(foodItem['text'], dbRestaurant['menuItems'])
                    tsv_writer.writerow([foodItem['text'], foodItem['match'], exactMatchStr, substringMatchStr, fuzzyMatchStr, partialMatchStr])

def exactMatch(food, menuItems):
    for menuItem in menuItems:
        if menuItem['name'].lower() == food.lower():
            return menuItem['name']
    return "None"

def substringMatch(food, menuItems):
    foundMatches = []
    for menuItem in menuItems:
        if(len(menuItem['name']) >= len(food)):
            if food.lower() in menuItem['name'].lower():
                foundMatches.append(menuItem['name'])
        else:
            if menuItem['name'].lower() in food.lower():
                foundMatches.append(menuItem['name'])
    
    if len(foundMatches) == 1:
        return foundMatches[0]

    return "None"

def fuzzyMatch(food, menuItems):
    foundMatches = []
    for menuItem in menuItems:
        foundMatches.append({'match' : menuItem['name'], 'jaro' : distance.get_jaro_distance(food.lower(), menuItem['name'].lower(), winkler=False, scaling=0.1)})
    
    max = foundMatches[0]
    for foundMatch in foundMatches[1:]:
        if foundMatch['jaro'] > max['jaro']:
            max = foundMatch   

    if max['jaro'] >= 0.9:
        return max['match']

    return "None"

def partialMatch(food, menuItems):
    foodTokenSet = set(stemmer.stem_arr(food))
    max = {'match' : "None", 'intersect_len' : -1}
    for menuItem in menuItems:
        menuItemTokenSet = set(stemmer.stem_arr(menuItem['name']))
        intersectionSet = foodTokenSet.intersection(menuItemTokenSet)
        
        if (len(intersectionSet) > max['intersect_len']) and (len(intersectionSet) > len(menuItemTokenSet)/2):
            max = {'match' : menuItem['name'], 'intersect_len' : len(intersectionSet) }

    return max['match']

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
    root = tk.Tk()
    root.withdraw()
    folderPath = filedialog.askdirectory()
    readAllFiles(folderPath)
    if(len(filePaths) > 0):
        processFiles(folderPath, filePaths)

if __name__ == "__main__":
    startProgram()
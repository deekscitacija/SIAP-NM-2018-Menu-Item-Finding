from pymongo import MongoClient
from bson.objectid import ObjectId
import tkinter as tk
from tkinter import filedialog
import xml.etree.cElementTree as xmlET
import os,re

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def convertFromMaeXmlToReldi(maeXmlsPath):
    for filename in os.listdir(maeXmlsPath):
        print("Processing " + filename)
        filepath = maeXmlsPath + "/" + filename
        if(os.path.isfile(filepath) and filename.endswith(".xml")):
            xmlRoot = xmlET.parse(filepath).getroot()
            tagsTag = xmlRoot.find("TAGS")
            if tagsTag is None:
                continue

            tags = tagsTag.getchildren()
            
            if len(tags) == 0:
                continue

            reviewId = filename.replace(".xml","")
            reviewIdQuery = {"_id" : ObjectId(reviewId)}
            review = db['FilteredAndTaggedRestaurantReviews'].find_one(reviewIdQuery)
            if review is None:
                continue

            sentences = review["sentences"]
            tokens = review["tokens"]
            namedEntities = review["namedEntities"]
            text = review["text"]

            partEnd = 0
            allPartEnds = 0
            for sentence in sentences["sentence"]:
                if(len(tags)==0):
                    break

                sentenceFirstToken = findFirstLastSentenceToken(sentence,tokens,True)
                if int(sentenceFirstToken["start"]) == 1 and partEnd > 0:
                    allPartEnds += partEnd
                    sentenceFirstTokenStartInText = text.find(sentenceFirstToken["text"],allPartEnds)
                    searchText = text[allPartEnds:sentenceFirstTokenStartInText]
                    partEnd += len(searchText)
                    allPartEnds += len(searchText)
                    for tag in tags:
                        tagOffset = tag.attrib.get("spans").split("~")
                        tagStart = int(tagOffset[0]) - partEnd
                        tagEnd = int(tagOffset[1]) - partEnd
                        tag.set("spans",str(tagStart) + "~" + str(tagEnd))
                        
                    partEnd = 0

                sentenceLastToken = findFirstLastSentenceToken(sentence,tokens,False)
                partEnd = int(sentenceLastToken["end"])
                tagsToRemove = []

                for tag in tags:
                    tagName = tag.tag
                    tagOffset = tag.attrib.get("spans").split("~")
                    tagStart = int(tagOffset[0])
                    tagEnd = int(tagOffset[1])
                    if tagStart < partEnd:
                        tokenNER = findNERtoken(sentence,namedEntities,tokens,tagStart+1,tagEnd)
                        tokenNER["value"] = tagName
                        tagsToRemove.append(tag)
                
                for tag in tagsToRemove:
                    tags.remove(tag)

            namedEntitiesUpdateQuery = {"$set" : {"namedEntities" : namedEntities}}
            db['FilteredAndTaggedRestaurantReviews'].update_one(reviewIdQuery,namedEntitiesUpdateQuery)

        elif(os.path.isdir(filepath)):
            convertFromMaeXmlToReldi(filepath)

def findFirstLastSentenceToken(sentence,tokens,first):
    sentenceTokens = sentence["tokenIDs"].split(" ")
    if first:
        sentenceTokenId = sentenceTokens[0]
    else:
        sentenceTokenId = sentenceTokens[-1]
    for token in tokens["token"]:
        if token["ID"] == sentenceTokenId:
            return token

def findTokenInSentence(sentence,token):
    sentenceTokens = sentence["tokenIDs"].split(" ")
    for sentenceToken in sentenceTokens:
        if sentenceToken == token["ID"]:
            return True

    return False

def findTokenByStartAndEnd(sentence,tokens,start,end):
    for token in tokens["token"]:
        if(int(token["start"]) == start and int(token["end"]) == end) and findTokenInSentence(sentence,token):
            return token

def findNERtoken(sentence,namedEntities,tokens,start,end):
    token = findTokenByStartAndEnd(sentence,tokens,start,end)
    for namedEntity in namedEntities["entity"]:
        if namedEntity["tokenIDs"] == token["ID"]:
            return namedEntity

def startConverting():
    root = tk.Tk()
    root.withdraw()
    maeXmlsPath = filedialog.askdirectory()
    convertFromMaeXmlToReldi(maeXmlsPath)

if __name__ == "__main__":
    startConverting()

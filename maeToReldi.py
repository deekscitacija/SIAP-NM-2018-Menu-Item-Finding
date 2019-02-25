from pymongo import MongoClient
from bson.objectid import ObjectId
import tkinter as tk
from tkinter import filedialog
import xml.etree.cElementTree as xmlET
import os

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def convertFromMaeXmlToReldi(maeXmlsPath):
    for filename in os.listdir(maeXmlsPath):
        filepath = maeXmlsPath + "/" + filename
        if(os.path.isfile(filepath) and filename.endswith(".xml")):
            xmlRoot = xmlET.parse(filepath).getroot()
            tags = xmlRoot.find("TAGS").getchildren()
            if len(tags) == 0:
                continue

            review = db['FilteredAndTaggedRestaurantReviews'].find_one({"_id" : ObjectId(filename.replace(".xml",""))})
            if review is None:
                continue

            sentences = review["sentences"]
            tokens = review["tokens"]
            namedEntities = review["namedEntities"]

            for sentence in sentences["sentence"]:
                if(len(tags)==0):
                    break

                sentenceLastToken = findLastSentenceToken(sentence,tokens)
                sentenceEnd = int(sentenceLastToken["end"])         
                tagsToRemove = []

                for tag in tags:
                    tagName = tag.tag
                    tagOffset = tag.attrib.get("spans").split("~")
                    tagStart = int(tagOffset[0])
                    tagEnd = int(tagOffset[1])
                    if tagStart <= sentenceEnd:
                        tokenNER = findNERtoken(sentence,namedEntities,tokens,tagStart+1,tagEnd)
                        tokenNER["value"] = tagName
                        tagsToRemove.append(tag)
                
                for tag in tagsToRemove:
                    tags.remove(tag)

                if len(tags) > 0:
                    minTagStart = findMinTagStart(tags)
                    sentenceEnd += minTagStart - sentenceEnd

                    for tag in tags:
                        tagOffset = tag.attrib.get("spans").split("~")
                        tagStart = int(tagOffset[0]) - sentenceEnd
                        tagEnd = int(tagOffset[1]) - sentenceEnd
                        tag.set("spans",str(tagStart) + "~" + str(tagEnd))

        elif(os.path.isdir(filepath)):
            convertFromMaeXmlToReldi(filepath)

def findLastSentenceToken(sentence,tokens):
    sentenceTokens = sentence["tokenIDs"].split(" ")
    sentenceLastTokenId = sentenceTokens[len(sentenceTokens)-1]
    for token in tokens["token"]:
        if token["ID"] == sentenceLastTokenId:
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

def findMinTagStart(tags):
    minTag = tags[0]
    minTagOffset = minTag.attrib.get("spans").split("~")
    minTagStart = int(minTagOffset[0])
    for tag in tags[1:]:
        tagOffset = tag.attrib.get("spans").split("~")
        tagStart = int(tagOffset[0])
        if tagStart < minTagStart:
            minTagStart = tagStart
        
    return minTagStart

def startConverting():
    root = tk.Tk()
    root.withdraw()
    maeXmlsPath = filedialog.askdirectory()
    convertFromMaeXmlToReldi(maeXmlsPath)

if __name__ == "__main__":
    startConverting()

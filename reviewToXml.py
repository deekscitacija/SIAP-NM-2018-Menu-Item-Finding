from pymongo import MongoClient
import xml.etree.cElementTree as xmlET
import tkinter as tk
from tkinter import filedialog

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def startProgram():
    startId = input("Unesite recenziju od koje cete da zapocnete generisanje Xml-a:")
    reviewNum = input("Unesite za koliko recenzija ce se vrsiti generisanje Xml-a:")
    try:
        startPoint = int(startId)
        endPoint = int(reviewNum)
        root = tk.Tk()
        root.withdraw()
        folderPath = filedialog.askdirectory()
        exportXml(startPoint, endPoint, folderPath)
    except ValueError:
        print("Unos neuspesan!")

def exportXml(startPoint, endPoint, folderPath):

    reviewCount = 0
    while(reviewCount < endPoint):
        reviewCount = reviewCount+1
        reviews = db['FilteredAndTaggedRestaurantReviews'].find()[startPoint:startPoint+1]
        
        for review in reviews:
            root = xmlET.Element("ReviewsTask")
            reviewText = xmlET.SubElement(root, "TEXT")
            reviewText.append(xmlET.Comment(' --><![CDATA[' + review["text"].replace(']]>', ']]]]><![CDATA[>') + ']]><!-- '))
            tags = xmlET.SubElement(root, "TAGS").text = " "

            tree = xmlET.ElementTree(root)
            tree.write(folderPath+"/"+str(review["_id"])+".xml", encoding='UTF-8', xml_declaration=True)

            startPoint = startPoint+1
        
if __name__ == "__main__":
    startProgram()
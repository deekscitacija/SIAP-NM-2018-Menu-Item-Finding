import tkinter as tk
import os
from tokeniser import generate_tokenizer, process, tokenize_sentences
from pymongo import MongoClient
from tkinter import filedialog
from alphabetConverter import serbianLatinToLatin

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def startProgram():
	root = tk.Tk()
	root.withdraw()
	filename = input("Unesite naziv fajle koja ce se izgenerisati:")
	folderPath = filedialog.askdirectory()
	startId = input("Unesite recenziju od koje cete da zapocnete tokenizovanje:")
	reviewNum = input("Unesite za koliko recenzija cete da odradite tokenizovanje:")
	try:
		startPoint = int(startId)
		endPoint = int(reviewNum)
		tokenizeReviews(startPoint,endPoint,folderPath,filename)
	except ValueError:
		print("Unos neuspesan!")

def tokenizeReviews(startPoint,endPoint,folderPath,filename):

	lang = 'sr'
	mode = 'standard'
	tokenizer=generate_tokenizer(lang)

	with open(os.path.join(folderPath,filename + "Original"),"w",encoding="utf-8") as outFileOriginal, open(os.path.join(folderPath,filename + "Converted"),"w",encoding="utf-8") as outFileConverted:
		reviewCount = 0
		while(reviewCount < endPoint):
			print("Processing: " + str(reviewCount))
			reviewCount+=1
			reviews = db['RestaurantReviews'].find()[startPoint:startPoint+1]
			if reviews.count() == 0:
				break

			for review in reviews:
				reviewText = getReviewContent(review)
				for reviewLine in reviewText.splitlines():
					sentences_tokens = tokenize_sentences(process[mode](tokenizer,reviewLine,lang))
					if sentences_tokens:
						for sentence_tokens in sentences_tokens:
							tokenizedSentence = " ".join(sentence_tokens)
							if tokenizedSentence and not tokenizedSentence.isspace():
								convertedTokenizedSentence = serbianLatinToLatin(tokenizedSentence)
								outFileOriginal.write(str(review["_id"]) + "\t" + tokenizedSentence + "\n")
								outFileConverted.write(str(review["_id"]) + "\t" + tokenizedSentence + "\n")
								if tokenizedSentence != convertedTokenizedSentence:
									outFileConverted.write(str(review["_id"]) + "\t" + convertedTokenizedSentence + "\n")

				startPoint+=1
	
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

    return reviewContent

if __name__=='__main__':
	startProgram()
			
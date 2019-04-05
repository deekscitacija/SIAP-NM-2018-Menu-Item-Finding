from tokeniser import generate_tokenizer, process, tokenize_sentences
from pymongo import MongoClient

client = MongoClient("mongodb+srv://MarijaIgor:SifrazaprojekatizSIAP-a!2018@cluster0-jndnv.azure.mongodb.net")
db = client['RestaurantData']

def startProgram():
	startId = input("Unesite recenziju od koje cete da zapocnete tokenizovanje:")
	reviewNum = input("Unesite za koliko recenzija cete da odradite tokenizovanje:")
	try:
		startPoint = int(startId)
		endPoint = int(reviewNum)
		tokenizeReviews(startPoint,endPoint)
	except ValueError:
		print("Unos neuspesan!")

def tokenizeReviews(startPoint,endPoint):

	lang = 'sr'
	mode = 'standard'
	tokenizer=generate_tokenizer(lang)

	reviewCount = 0
	while(reviewCount < endPoint):
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
						print(" ".join(sentence_tokens))

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
			
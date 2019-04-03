import tokeniser

if __name__=='__main__':
	#import argparse
	#parser=argparse.ArgumentParser(description='Tokeniser for (non-)standard Slovene, Croatian and Serbian')
	#parser.add_argument('lang',help='language of the text',choices=['sl','hr','sr'])
	#parser.add_argument('-n','--nonstandard',help='invokes the non-standard mode',action='store_true')
	#args=parser.parse_args()
	#lang=args.lang
	#mode='standard'
	#if args.nonstandard:
		#mode='nonstandard'
	
	lang = 'sr'
	mode = 'nonstandard'
	tokenizer=tokeniser.generate_tokenizer(lang)
	par_id=0
	with open("example.txt", "r", encoding="utf-8") as exampleFile, open("out.txt", "w", encoding="utf-8") as outFile :
		for line in exampleFile:
			par_id+=1
			outFile.write(tokeniser.represent_tomaz(tokeniser.process[mode](tokenizer,line,lang),par_id))
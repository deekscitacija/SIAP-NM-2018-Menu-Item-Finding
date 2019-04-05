from tokeniser import generate_tokenizer, process, tokenize_sentences

if __name__=='__main__':
	
	lang = 'sr'
	mode = 'standard'
	tokenizer=generate_tokenizer(lang)

	with open("example.txt", "r", encoding="utf-8") as exampleFile:
		for line in exampleFile:
			sentences_tokens = tokenize_sentences(process[mode](tokenizer,line,lang))
			if sentences_tokens:
				print(sentences_tokens)
			
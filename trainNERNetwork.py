import tkinter as tk
from tkinter import filedialog
from readConllevalFile import readConllevalFile

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    with open(filepath,"r",encoding="utf-8") as conllevalFile:
        sentences = readConllevalFile(conllevalFile, '\t', [0,1,9])
        sentences_words = []
        tags = set()
        
        for sentence in sentences:
                sentence_words = []
                for sentenceElement in sentence:
                        sentence_words.append(sentenceElement[1])
                        tags.add(sentenceElement[-1])
                sentences_words.append(sentence_words)

        max_len = 200
        sentence_words_padded = padSentenceWords(sentences_words, max_len)
        print(sentence_words_padded[1])

        tag2idx = {t: i for i, t in enumerate(tags)}

def padSentenceWords(sentences_words, max_len):
        sentences_words_padded = []
        for sentence_words in sentences_words:
                sentence_words_padded = []
                for i in range(max_len):
                        try:
                                sentence_words_padded.append(sentence_words[i])
                        except:
                                sentence_words_padded.append("__PAD__")
                sentences_words_padded.append(sentence_words_padded)
        return sentences_words_padded

if __name__ == "__main__":
    startProgram()
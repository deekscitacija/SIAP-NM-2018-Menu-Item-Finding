import tkinter as tk
from tkinter import filedialog
from readConllevalFile import readConllevalFile
from keras.preprocessing.sequence import pad_sequences

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename()
    with open(filepath,"r",encoding="utf-8") as conllevalFile:
        sentences = readConllevalFile(conllevalFile, '\t', [0,1,9])
        sentences_words = []
        sentences_tags = []
        tags = set()
        
        for sentence in sentences:
                sentence_words = []
                sentence_tags = []
                for sentenceElement in sentence:
                        sentence_words.append(sentenceElement[1])
                        sentence_tag = sentenceElement[-1]
                        sentence_tags.append(sentence_tag)
                        tags.add(sentence_tag)
                sentences_words.append(sentence_words)
                sentences_tags.append(sentence_tags)

        max_len = 200
        tag2idx = {t: i for i, t in enumerate(list(tags))}
        sentence_words_padded = padSentenceWords(sentences_words, max_len)
        sentence_tags_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags]
        sentence_tags_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_converted, padding="post", value=tag2idx["O"])

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
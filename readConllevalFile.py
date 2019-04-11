import csv

def readConllevalFile(file, fileDelimiter, columns):
    reader = csv.reader(file, delimiter = fileDelimiter)
    sentences = []
    sentence = []

    for line in reader:
        if len(line) == 0:
            sentences.append(sentence)
        else:
            sentenceElement = []
            for i,column in enumerate(line):
                if i in columns:
                    sentenceElement.append(column)
                    sentence.append(sentenceElement)

    return sentences
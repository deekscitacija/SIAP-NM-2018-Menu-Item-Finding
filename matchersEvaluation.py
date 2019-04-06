import csv
import tkinter as tk
from tkinter import filedialog
from sklearn.metrics import classification_report,precision_score,recall_score,f1_score

COL_NUMBER = 6

def startProgram():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    readModelsFile(filename)

def readModelsFile(filename):
    with open(filename,"r",encoding="utf-8") as modelsFile:
        tsv_reader = csv.reader(modelsFile,delimiter="\t")
        expectedResults = []
        exactMatchResults = []
        substringMatchResults = []
        fuzzyMatchResults = []
        partialMatchResults = []
        for line in tsv_reader:
            if(len(line)==COL_NUMBER):
                expectedResults.append(line[1])
                exactMatchResults.append(line[2])
                substringMatchResults.append(line[3])
                fuzzyMatchResults.append(line[4])
                partialMatchResults.append(line[5])
        
        evaluateModels(expectedResults,exactMatchResults,substringMatchResults,fuzzyMatchResults,partialMatchResults)

def evaluateModels(expectedResults,exactMatchResults,substringMatchResults,fuzzyMatchResults,partialMatchResults):
    evaluateModel("exactMatch",expectedResults,exactMatchResults)
    evaluateModel("substringMatch",expectedResults,substringMatchResults)
    evaluateModel("fuzzyMatch",expectedResults,fuzzyMatchResults)
    evaluateModel("partialMatch",expectedResults,partialMatchResults)

def evaluateModel(matchType,expectedResults,matchResults):
    print("Results for "+matchType+":")
    print("Precision: " + str(precision_score(expectedResults,matchResults,average='weighted')))
    print("Recall: " + str(recall_score(expectedResults,matchResults,average='weighted')))
    print("F1: " + str(f1_score(expectedResults,matchResults,average='weighted')))

if __name__ == "__main__":
    startProgram()
import tkinter as tk
from tkinter import filedialog
from readConllevalFile import readConllevalFile
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.models import Model, Input
from keras.layers import LSTM, GRU, Embedding, Dense, TimeDistributed, Dropout, Bidirectional, Conv1D, concatenate, SpatialDropout1D, GlobalMaxPooling1D
from keras_contrib.layers import CRF
from statistics import median
import matplotlib.pyplot as plt
from ordered_set import OrderedSet
import numpy as np
import h5py
import os
import csv

models_path = "nnModels"
tags_set = OrderedSet(["O", "B-FOOD", "I-FOOD", "L-FOOD", "U-FOOD"])

def startProgram():

    root = tk.Tk()
    root.withdraw()
    optionString = input("Choose option:\n1 - Analyze word and sentence lengths\n2 - Train\n3 - Test\nYour choise: ")
    try:
        option = int(optionString)
        if option not in [1,2,3]:
                return
    except ValueError:
        print("Niste uneli broj")
        return
    if option != 1:
        modelOptionString = input("Choose option:\n1 - GRU One Hot\n2 - GRU CRF\nYour choise: ")
        try:
                modelOption = int(modelOptionString)
                if modelOption not in [1,2,3,4]:
                        return
        except ValueError:
                print("Niste uneli broj")
                return

    filepathTrain = filedialog.askopenfilename()
    filepathTest = filedialog.askopenfilename()
    with open(filepathTrain,"r", encoding="utf-8") as conllevalFileTrain, open(filepathTest,"r", encoding="utf-8") as conllevalFileTest:
        sentences_train = readConllevalFile(conllevalFileTrain, '\t', [0,1,12])
        sentences_test = readConllevalFile(conllevalFileTest, '\t', [0,1,12])
        sentences_words_train = []
        sentences_tags_train = []
        sentences_words_test = []
        sentences_tags_test = []
        words_set = OrderedSet()
        #tags_set = OrderedSet()

        for sentence in sentences_train:
                sentence_words = []
                sentence_tags = []
                for sentenceElement in sentence:
                        sentence_word = sentenceElement[1]
                        sentence_words.append(sentence_word)
                        words_set.add(sentence_word)
                        sentence_tag = sentenceElement[-1]
                        sentence_tags.append(sentence_tag)
                        #tags.add(sentence_tag)
                sentences_words_train.append(sentence_words)
                sentences_tags_train.append(sentence_tags)

        for sentence in sentences_test:
                sentence_words = []
                sentence_tags = []
                for sentenceElement in sentence:
                        sentence_word = sentenceElement[1]
                        sentence_words.append(sentence_word)
                        words_set.add(sentence_word)
                        sentence_tag = sentenceElement[-1]
                        sentence_tags.append(sentence_tag)
                        #tags.add(sentence_tag)
                sentences_words_test.append(sentence_words)
                sentences_tags_test.append(sentence_tags)

        words = list(words_set)
        words.append("ENDPAD")
        tags = list(tags_set)
        n_words = len(words)
        n_tags = len(tags)
        word2idx = {w: i+1 for i, w in enumerate(words)}
        tag2idx = {t: i for i, t in enumerate(tags)}

        if option == 1:
                analyzeWordAndSentenceLength(words, sentences_words_train + sentences_words_test)
        else:
                max_len_str = input("Unesite maksimalnu duzinu recenice: ")
                try:
                        max_len = int(max_len_str)
                except ValueError:
                        print("Niste uneli broj")
                        return

                output_dim_str = input("Unesite output dim: ")
                try:
                        output_dim = int(output_dim_str)
                except ValueError:
                        print("Niste uneli broj")
                        return

                #sentence_words_padded = padSentenceWords(sentences_words, max_len)
                sentence_words_train_converted = [[word2idx[sentence_word] for sentence_word in sentence_words] for sentence_words in sentences_words_train]
                sentence_words_train_padded = pad_sequences(maxlen=max_len, sequences=sentence_words_train_converted, padding="post", truncating="post", value=word2idx['ENDPAD'])
                sentence_words_test_converted = [[word2idx[sentence_word] for sentence_word in sentence_words] for sentence_words in sentences_words_test]
                sentence_words_test_padded = pad_sequences(maxlen=max_len, sequences=sentence_words_test_converted, padding="post", truncating="post", value=word2idx['ENDPAD'])
                sentence_tags_train_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags_train]
                sentence_tags_train_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_train_converted, padding="post", truncating="post", value=tag2idx["O"])
                sentence_tags_test_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags_test]
                sentence_tags_test_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_test_converted, padding="post", truncating="post", value=tag2idx["O"])
                sentence_tags_train_padded_categorical = [to_categorical(sentence_tag_train_padded, num_classes=n_tags) for sentence_tag_train_padded in sentence_tags_train_padded]

                if option == 1:
                        file_name = input("Unesite naziv fajle u kojoj ce biti sacuvane tezine: ")
                        if modelOption == 1:
                                trainNERModelGru(max_len, n_words, n_tags, output_dim, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 2:
                                trainNERModelGruCRF(max_len, n_words, n_tags, output_dim, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                elif option == 2:
                        model_weights = filedialog.askopenfilename()
                        if modelOption == 1:
                                testNERModelGru(max_len, n_words, n_tags, output_dim, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights)
                        elif modelOption == 2:
                                testNERModelGruCRF(max_len, n_words, n_tags, output_dim, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights)

def createNERModelGru(max_len, n_words, n_tags, output_dim):
        input = Input(shape=(max_len,))
        model = Embedding(input_dim=n_words + 1, output_dim=output_dim, input_length=max_len, mask_zero=True)(input)
        model = Dropout(0.1)(model)
        model = Bidirectional(GRU(units=100, return_sequences=True, recurrent_dropout=0.1))(model)
        out = TimeDistributed(Dense(n_tags, activation="softmax"))(model)
        model = Model(input, out)

        return model

def trainNERModelGru(max_len, n_words, n_tags, output_dim, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):   
        model = createNERModelGru(max_len, n_words, n_tags, output_dim)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
        model.fit(sentence_words_train_padded, np.array(sentence_tags_train_padded_categorical), batch_size=32, epochs=5, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

def testNERModelGru(max_len, n_words, n_tags, output_dim, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights):
        model = createNERModelGru(max_len, n_words, n_tags, output_dim)
        model.load_weights(model_weights)

        with open(os.path.join(models_path, model_weights.replace(".h5py", "") + "Results"), "w") as resultsFile:
                tsv_writer = csv.writer(resultsFile, delimiter="\t", lineterminator='\n')
                for i, sentence_word_test_padded in enumerate(sentence_words_test_padded):       
                        pad_start = findPadStart(sentence_word_test_padded, words)
                        predictions = model.predict(np.array([sentence_word_test_padded]))
                        predictions = np.argmax(predictions, axis=-1)
                        for word, expected, prediction in zip(sentence_word_test_padded[:pad_start], sentence_tags_test_padded[i][:pad_start], predictions[0][:pad_start]):
                                 if word != 0:
                                        tsv_writer.writerow([words[word-1], tags[expected], tags[prediction]])
                        resultsFile.write("\n")

def createNERModelGruCRF(max_len, n_words, n_tags, output_dim):
        input = Input(shape=(max_len,))
        model = Embedding(input_dim=n_words + 1, output_dim=output_dim, input_length=max_len, mask_zero=True)(input)
        model = Bidirectional(GRU(units=50, return_sequences=True, recurrent_dropout=0.1))(model)
        model = TimeDistributed(Dense(50, activation="relu"))(model)
        crf = CRF(n_tags)
        out = crf(model)
        model = Model(input, out)

        return (model, crf)

def trainNERModelGruCRF(max_len, n_words, n_tags, output_dim, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):   
        (model, crf) = createNERModelGruCRF(max_len, n_words, n_tags, output_dim)
        model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
        model.fit(sentence_words_train_padded, np.array(sentence_tags_train_padded_categorical), batch_size=32, epochs=5, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

def testNERModelGruCRF(max_len, n_words, n_tags, output_dim, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights):
        modelCRF = createNERModelGruCRF(max_len, n_words, n_tags, output_dim)
        model = modelCRF[0]
        model.load_weights(model_weights)

        with open(os.path.join(models_path, model_weights.replace(".h5py", "") + "Results"), "w") as resultsFile:
                tsv_writer = csv.writer(resultsFile, delimiter="\t", lineterminator='\n')
                for i, sentence_word_test_padded in enumerate(sentence_words_test_padded):       
                        pad_start = findPadStart(sentence_word_test_padded, words)
                        predictions = model.predict(np.array([sentence_word_test_padded]))
                        predictions = np.argmax(predictions, axis=-1)
                        for word, expected, prediction in zip(sentence_word_test_padded[:pad_start], sentence_tags_test_padded[i][:pad_start], predictions[0][:pad_start]):
                                if word != 0:
                                        tsv_writer.writerow([words[word-1], tags[expected], tags[prediction]])
                        resultsFile.write("\n")

def createNERModelGruCharacter(max_len, max_len_char, n_chars, n_words, n_tags, output_dim):
        word_in = Input(shape=(max_len,))
        emb_word = Embedding(input_dim=n_words + 2, output_dim=20, input_length=max_len, mask_zero=True)(word_in)
        char_in = Input(shape=(max_len, max_len_char,))
        emb_char = TimeDistributed(Embedding(input_dim=n_chars + 2, output_dim=10, input_length=max_len_char, mask_zero=True))(char_in)
        char_enc = TimeDistributed(LSTM(units=20, return_sequences=False, recurrent_dropout=0.5))(emb_char)
        x = concatenate([emb_word, char_enc])
        x = SpatialDropout1D(0.3)(x)
        main_lstm = Bidirectional(GRU(units=50, return_sequences=True, recurrent_dropout=0.6))(x)
        out = TimeDistributed(Dense(n_tags + 1, activation="softmax"))(main_lstm)
        model = Model([word_in, char_in], out)

        return model

def traineNERModelGruCharacter(max_len, max_len_char, n_chars, n_words, n_tags, output_dim, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):  
        model = createNERModelGruCharacter(max_len, max_len_char, n_chars, n_words, n_tags, output_dim)
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["acc"])
        model.fit([sentence_words_train_padded, np.array(sentence_chars_train_padded).reshape((len(sentence_chars_train_padded), max_len, max_len_char))], np.array(sentence_tags_train_padded_categorical).reshape(len(sentence_tags_train_padded_categorical), max_len, 1), batch_size=32, epochs=10, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

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

def findPadStart(sentence_words, words):
        for i, word in enumerate(sentence_words):
                if word != 0:
                        if words[word-1] == "ENDPAD":
                                return i

def analyzeWordAndSentenceLength(words, sentences_words):
        sentence_lens = []
        word_lens = []
        for word in words:
                word_lens.append(len(word))

        for sentence_words in sentences_words:
                sentence_lens.append(len(sentence_words))

        print("Average word length", sum(word_lens) / len(word_lens))
        print("Max word length", max(word_lens))
        print("Median word length", median(word_lens))

        print("Average sentence length", sum(sentence_lens) / len(sentence_lens))
        print("Max sentence length", max(sentence_lens))
        print("Median sentence length", median(sentence_lens))

        plt.title("Word length distribution")
        plt.xlabel("Word length range")
        plt.ylabel("Number of occurences")
        plt.hist(word_lens, bins=20)

        plt.title("Sentence length distribution")
        plt.xlabel("Sentence length range")
        plt.ylabel("Number of occurences")
        plt.hist(sentence_lens, bins=50)
        plt.show()

        input()

if __name__ == "__main__":
    startProgram()
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
        modelOptionString = input("Choose option:\n1 - GRU One Hot\n2 - GRU CRF One Hot\n3 - GRU Character Embeddings\n4 - GRU CRF Character Embeddings\n5 - LSTM One Hot\n6 - LSTM CRF One Hot\n7 - LSTM Character Embeddings\n8 - LSTM CRF Character Embeddings\nYour choise: ")
        try:
                modelOption = int(modelOptionString)
                if modelOption not in [1,2,3,4,5,6,7,8]:
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
        #words.append("ENDPAD")
        tags = list(tags_set)
        n_words = len(words)
        n_tags = len(tags)
        word2idx = {w: i + 2 for i, w in enumerate(words)}
        word2idx["UNK"] = 1
        word2idx["PAD"] = 0
        tag2idx = {t: i + 1 for i, t in enumerate(tags)}
        tag2idx["PAD"] = 0
        chars_set = set([w_i for w in words for w_i in w])
        chars = list(chars_set)
        #chars.append("ENDPAD")
        n_chars = len(chars)
        char2idx = {c: i + 2 for i, c in enumerate(chars)}
        char2idx["UNK"] = 1
        char2idx["PAD"] = 0

        if option == 1:
                analyzeWordAndSentenceLength(words, sentences_words_train + sentences_words_test)
        else:
                max_len_str = input("Unesite maksimalnu duzinu recenice: ")
                try:
                        max_len = int(max_len_str)
                except ValueError:
                        print("Niste uneli broj")
                        return
                
                if modelOption in [3,4]:
                        max_len_char_str = input("Unesite maksimalnu duzinu reci: ")
                        try:
                                max_len_char = int(max_len_char_str)
                        except ValueError:
                                print("Niste uneli broj")
                                return 

                output_dim_word_str = input("Unesite output dim reci: ")
                try:
                        output_dim_word = int(output_dim_word_str)
                except ValueError:
                        print("Niste uneli broj")
                        return

                if modelOption in [3,4]:
                        output_dim_char_str = input("Unesite output dim karaktera: ")
                        try:
                                output_dim_char = int(output_dim_char_str)
                        except ValueError:
                                print("Niste uneli broj")
                                return

                #sentence_words_padded = padSentenceWords(sentences_words, max_len)
                sentence_words_train_converted = [[word2idx[sentence_word] for sentence_word in sentence_words] for sentence_words in sentences_words_train]
                sentence_words_train_padded = pad_sequences(maxlen=max_len, sequences=sentence_words_train_converted, padding="post", truncating="post", value=word2idx['PAD'])
                sentence_words_test_converted = [[word2idx[sentence_word] for sentence_word in sentence_words] for sentence_words in sentences_words_test]
                sentence_words_test_padded = pad_sequences(maxlen=max_len, sequences=sentence_words_test_converted, padding="post", truncating="post", value=word2idx['PAD'])
                sentence_tags_train_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags_train]
                sentence_tags_train_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_train_converted, padding="post", truncating="post", value=tag2idx["PAD"])
                sentence_tags_test_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags_test]
                sentence_tags_test_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_test_converted, padding="post", truncating="post", value=tag2idx["PAD"])
                sentence_tags_train_padded_categorical = [to_categorical(sentence_tag_train_padded, num_classes=n_tags + 1) for sentence_tag_train_padded in sentence_tags_train_padded]
                
                if modelOption in [3,4]:
                        sentence_chars_train_padded = padSentenceChars(sentences_words_train, max_len, max_len_char, char2idx)
                        sentence_chars_test_padded = padSentenceChars(sentences_words_test, max_len, max_len_char, char2idx)      

                if option == 2:
                        file_name = input("Unesite naziv fajle u kojoj ce biti sacuvane tezine: ")
                        if modelOption == 1:
                                trainNERModelLstmGru(True, max_len, n_words, n_tags, output_dim_word, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 2:
                                trainNERModelLstmGruCRF(True, max_len, n_words, n_tags, output_dim_word, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 3:
                                trainNERModelLstmGruCharacter(True, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 4:
                                trainNERModelLstmGruCRFCharacter(True, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 5:
                                trainNERModelLstmGru(False, max_len, n_words, n_tags, output_dim_word, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 6:
                                trainNERModelLstmGruCRF(False, max_len, n_words, n_tags, output_dim_word, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 7:
                                trainNERModelLstmGruCharacter(False, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                        elif modelOption == 8:
                                trainNERModelLstmGruCRFCharacter(False, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name)
                elif option == 3:
                        model_weights = filedialog.askopenfilename()
                        if modelOption == 1:
                                testNERModelLstmGru(True, max_len, n_words, n_tags, output_dim_word, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights)
                        elif modelOption == 2:
                                testNERModelLstmGruCRF(True, max_len, n_words, n_tags, output_dim_word, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights)
                        elif modelOption == 3:
                                testNERModelLstmGruCharacter(True, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_test_padded, sentence_words_test_padded, sentence_tags_test_padded, words, tags, chars, model_weights)
                        elif modelOption == 4:
                                testNERModelLstmGruCRFCharacter(True, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_test_padded, sentence_words_test_padded, sentence_tags_test_padded, words, tags, chars, model_weights)
                        elif modelOption == 5:
                                testNERModelLstmGru(False, max_len, n_words, n_tags, output_dim_word, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights)
                        elif modelOption == 6:
                                testNERModelLstmGruCRF(False, max_len, n_words, n_tags, output_dim_word, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights)
                        elif modelOption == 7:
                                testNERModelLstmGruCharacter(False, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_test_padded, sentence_words_test_padded, sentence_tags_test_padded, words, tags, chars, model_weights)
                        elif modelOption == 8:
                                testNERModelLstmGruCRFCharacter(False, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_test_padded, sentence_words_test_padded, sentence_tags_test_padded, words, tags, chars, model_weights)

def createNERModelLstmGru(gru, max_len, n_words, n_tags, output_dim_word):
        input = Input(shape=(max_len,))
        model = Embedding(input_dim=n_words + 2, output_dim=output_dim_word, input_length=max_len, mask_zero=True)(input)
        model = Dropout(0.1)(model)
        if gru:
                model = Bidirectional(GRU(units=100, return_sequences=True, recurrent_dropout=0.1))(model)
        else:
                model = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.1))(model)  
        out = TimeDistributed(Dense(n_tags + 1, activation="softmax"))(model)
        model = Model(input, out)

        return model

def trainNERModelLstmGru(gru, max_len, n_words, n_tags, output_dim_word, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):   
        model = createNERModelLstmGru(gru, max_len, n_words, n_tags, output_dim_word)

        model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["accuracy"])
        model.fit(sentence_words_train_padded, np.array(sentence_tags_train_padded_categorical), batch_size=32, epochs=5, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

def testNERModelLstmGru(gru, max_len, n_words, n_tags, output_dim_word, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights):
        model = createNERModelLstmGru(gru, max_len, n_words, n_tags, output_dim_word)
        model.load_weights(model_weights)

        with open(os.path.join(models_path, model_weights.replace(".h5py", "") + "Results"), "w") as resultsFile:
                tsv_writer = csv.writer(resultsFile, delimiter="\t", lineterminator='\n')
                predictions = model.predict([sentence_words_test_padded])
                for i, (sentence_word_test_padded, sentence_tag_test_padded) in enumerate(zip(sentence_words_test_padded, sentence_tags_test_padded)):       
                        pad_start = findPadStartWords(sentence_word_test_padded)
                        predictions_item = np.argmax(predictions[i], axis=-1)
                        for word, expected, prediction in zip(sentence_word_test_padded[:pad_start], sentence_tag_test_padded[:pad_start], predictions_item[:pad_start]):
                                 if word != 0:
                                        tsv_writer.writerow([words[word-2], tags[expected-1], tags[prediction-1]])
                        resultsFile.write("\n")

def createNERModelLstmGruCRF(gru, max_len, n_words, n_tags, output_dim_word):
        input = Input(shape=(max_len,))
        model = Embedding(input_dim=n_words + 2, output_dim=output_dim_word, input_length=max_len, mask_zero=True)(input)
        if gru:
                model = Bidirectional(GRU(units=50, return_sequences=True, recurrent_dropout=0.1))(model)
        else:
                model = Bidirectional(LSTM(units=50, return_sequences=True, recurrent_dropout=0.1))(model) 
        model = TimeDistributed(Dense(50, activation="relu"))(model)
        crf = CRF(n_tags + 1)
        out = crf(model)
        model = Model(input, out)

        return (model, crf)

def trainNERModelLstmGruCRF(gru, max_len, n_words, n_tags, output_dim_word, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):   
        (model, crf) = createNERModelLstmGruCRF(gru, max_len, n_words, n_tags, output_dim_word)
        model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
        model.fit(sentence_words_train_padded, np.array(sentence_tags_train_padded_categorical), batch_size=32, epochs=5, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

def testNERModelLstmGruCRF(gru, max_len, n_words, n_tags, output_dim_word, sentence_words_test_padded, sentence_tags_test_padded, words, tags, model_weights):
        modelCRF = createNERModelLstmGruCRF(gru, max_len, n_words, n_tags, output_dim_word)
        model = modelCRF[0]
        model.load_weights(model_weights)

        with open(os.path.join(models_path, model_weights.replace(".h5py", "") + "Results"), "w") as resultsFile:
                tsv_writer = csv.writer(resultsFile, delimiter="\t", lineterminator='\n')
                predictions = model.predict([sentence_words_test_padded])
                for i, (sentence_word_test_padded, sentence_tag_test_padded) in enumerate(zip(sentence_words_test_padded, sentence_tags_test_padded)):       
                        pad_start = findPadStartWords(sentence_word_test_padded)
                        predictions_item = np.argmax(predictions[i], axis=-1)
                        for word, expected, prediction in zip(sentence_word_test_padded[:pad_start], sentence_tag_test_padded[:pad_start], predictions_item[:pad_start]):
                                if word != 0:
                                        tsv_writer.writerow([words[word-2], tags[expected-1], tags[prediction-1]])
                        resultsFile.write("\n")

def createNERModelLstmGruCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char):
        word_in = Input(shape=(max_len,))
        emb_word = Embedding(input_dim=n_words + 2, output_dim=output_dim_word, input_length=max_len, mask_zero=True)(word_in)
        char_in = Input(shape=(max_len, max_len_char,))
        emb_char = TimeDistributed(Embedding(input_dim=n_chars + 2, output_dim=output_dim_char, input_length=max_len_char, mask_zero=True))(char_in)
        if gru:
                char_enc = TimeDistributed(GRU(units=20, return_sequences=False, recurrent_dropout=0.5))(emb_char)
        else:
                char_enc = TimeDistributed(LSTM(units=20, return_sequences=False, recurrent_dropout=0.5))(emb_char)
        x = concatenate([emb_word, char_enc])
        x = SpatialDropout1D(0.3)(x)
        if gru:
                main_lstm_gru = Bidirectional(GRU(units=100, return_sequences=True, recurrent_dropout=0.6))(x)
        else:
                main_lstm_gru = Bidirectional(LSTM(units=100, return_sequences=True, recurrent_dropout=0.6))(x)
        out = TimeDistributed(Dense(n_tags + 1, activation="softmax"))(main_lstm_gru)
        model = Model([word_in, char_in], out)

        return model

def trainNERModelLstmGruCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):  
        model = createNERModelLstmGruCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char)
        model.compile(optimizer="rmsprop", loss="categorical_crossentropy", metrics=["acc"])
        model.fit([sentence_words_train_padded, np.array(sentence_chars_train_padded).reshape((len(sentence_chars_train_padded), max_len, max_len_char))], np.array(sentence_tags_train_padded_categorical).reshape(len(sentence_tags_train_padded_categorical), max_len, n_tags + 1), batch_size=32, epochs=5, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

def testNERModelLstmGruCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_test_padded, sentence_words_test_padded, sentence_tags_test_padded, words, tags, chars, model_weights):
        model = createNERModelLstmGruCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char)
        model.load_weights(model_weights)

        with open(os.path.join(models_path, model_weights.replace(".h5py", "") + "Results"), "w") as resultsFile:
                tsv_writer = csv.writer(resultsFile, delimiter="\t", lineterminator='\n')
                predictions = model.predict([sentence_words_test_padded, np.array(sentence_chars_test_padded).reshape((len(sentence_chars_test_padded), max_len, max_len_char))])
                for i, (sentence_word_test_padded, sentence_tag_test_padded) in enumerate(zip(sentence_words_test_padded, sentence_tags_test_padded)):       
                        pad_start = findPadStartWords(sentence_word_test_padded)
                        predictions_item = np.argmax(predictions[i], axis=-1)
                        for word, expected, prediction in zip(sentence_word_test_padded[:pad_start], sentence_tag_test_padded[:pad_start], predictions_item[:pad_start]):
                                if word != 0:
                                        tsv_writer.writerow([words[word-2], tags[expected-1], tags[prediction-1]])
                        resultsFile.write("\n")

def createNERModelLstmGruCRFCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char):
        word_in = Input(shape=(max_len,))
        emb_word = Embedding(input_dim=n_words + 2, output_dim=output_dim_word, input_length=max_len, mask_zero=True)(word_in)
        char_in = Input(shape=(max_len, max_len_char,))
        emb_char = TimeDistributed(Embedding(input_dim=n_chars + 2, output_dim=output_dim_char, input_length=max_len_char, mask_zero=True))(char_in)
        if gru:
                char_enc = TimeDistributed(GRU(units=20, return_sequences=False, recurrent_dropout=0.5))(emb_char)
        else:
                char_enc = TimeDistributed(LSTM(units=20, return_sequences=False, recurrent_dropout=0.5))(emb_char)
        x = concatenate([emb_word, char_enc])
        x = SpatialDropout1D(0.3)(x)
        if gru:
                main_lstm_gru = Bidirectional(GRU(units=50, return_sequences=True, recurrent_dropout=0.6))(x)
        else:
                main_lstm_gru = Bidirectional(LSTM(units=50, return_sequences=True, recurrent_dropout=0.6))(x)
        model = TimeDistributed(Dense(50, activation="relu"))(main_lstm_gru)
        crf = CRF(n_tags + 1)
        out = crf(model)
        model = Model([word_in, char_in], out)

        return (model, crf)

def trainNERModelLstmGruCRFCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_train_padded, sentence_words_train_padded, sentence_tags_train_padded_categorical, file_name):  
        (model, crf) = createNERModelLstmGruCRFCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char)
        model.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
        model.fit([sentence_words_train_padded, np.array(sentence_chars_train_padded).reshape((len(sentence_chars_train_padded), max_len, max_len_char))], np.array(sentence_tags_train_padded_categorical).reshape(len(sentence_tags_train_padded_categorical), max_len, n_tags + 1), batch_size=32, epochs=5, verbose=2)

        model.save_weights(os.path.join(models_path, file_name + ".h5py"), overwrite=True)

def testNERModelLstmGruCRFCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char, sentence_chars_test_padded, sentence_words_test_padded, sentence_tags_test_padded, words, tags, chars, model_weights):
        modelCRF = createNERModelLstmGruCRFCharacter(gru, max_len, max_len_char, n_chars, n_words, n_tags, output_dim_word, output_dim_char)
        model = modelCRF[0]
        model.load_weights(model_weights)

        with open(os.path.join(models_path, model_weights.replace(".h5py", "") + "Results"), "w") as resultsFile:
                tsv_writer = csv.writer(resultsFile, delimiter="\t", lineterminator='\n')
                predictions = model.predict([sentence_words_test_padded, np.array(sentence_chars_test_padded).reshape((len(sentence_chars_test_padded), max_len, max_len_char))])
                for i, (sentence_word_test_padded, sentence_tag_test_padded) in enumerate(zip(sentence_words_test_padded, sentence_tags_test_padded)):       
                        pad_start = findPadStartWords(sentence_word_test_padded)
                        predictions_item = np.argmax(predictions[i], axis=-1)
                        for word, expected, prediction in zip(sentence_word_test_padded[:pad_start], sentence_tag_test_padded[:pad_start], predictions_item[:pad_start]):
                                if word != 0:
                                        tsv_writer.writerow([words[word-2], tags[expected-1], tags[prediction-1]])
                        resultsFile.write("\n")
        
def padSentenceChars(sentences_words, max_len, max_len_char, char2idx):
        sentences_chars_padded = []
        for sentence_words in sentences_words:
                sentence_sequence = []
                for i in range(max_len):
                        word_sequence = []
                        for j in range(max_len_char):
                                try:
                                        word_sequence.append(char2idx.get(sentence_words[i][j]))
                                except:
                                        word_sequence.append(char2idx.get("PAD"))
                        sentence_sequence.append(word_sequence)
                sentences_chars_padded.append(np.array(sentence_sequence))
        return sentences_chars_padded

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

def findPadStartWords(sentence_words):
        for i, word in enumerate(sentence_words):
                if word == 0:
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
import tkinter as tk
from tkinter import filedialog
from readConllevalFile import readConllevalFile
from keras.preprocessing.sequence import pad_sequences
from ordered_set import OrderedSet
import torch
from torch.optim import Adam
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from pytorch_pretrained_bert import BertTokenizer, BertConfig
from pytorch_pretrained_bert import BertForTokenClassification, BertAdam
#from pytorch_pretrained_bert import WEIGHTS_NAME, CONFIG_NAME
from tqdm import tqdm, trange
import numpy as np
import h5py
import os
import csv

#models_path = "nnModels"
output_model_file = "nnModels/bert_model_file.bin"
output_config_file = "nnModels/bert_config_file.bin"
tags_set = OrderedSet(["O", "B-FOOD", "I-FOOD", "L-FOOD", "U-FOOD"])
batch_size = 8

def startProgram():

    root = tk.Tk()
    root.withdraw()
    optionString = input("Choose option:\n1 - Train\n2 - Test\nYour choise: ")
    try:
        option = int(optionString)
        if option not in [1,2]:
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
        word2idx = {w: i for i, w in enumerate(words)}
        tag2idx = {t: i for i, t in enumerate(tags)}

        max_len_str = input("Unesite maksimalnu duzinu recenice: ")
        try:
            max_len = int(max_len_str)
        except ValueError:
            print("Niste uneli broj")
            return

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        sentence_words_train_converted = [[word2idx[sentence_word] for sentence_word in sentence_words] for sentence_words in sentences_words_train]
        sentence_words_train_padded = pad_sequences(maxlen=max_len, sequences=sentence_words_train_converted, dtype="long", padding="post", truncating="post")
        sentence_words_test_converted = [[word2idx[sentence_word] for sentence_word in sentence_words] for sentence_words in sentences_words_test]
        sentence_words_test_padded = pad_sequences(maxlen=max_len, sequences=sentence_words_test_converted, dtype="long", padding="post", truncating="post")
        sentence_tags_train_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags_train]
        sentence_tags_train_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_train_converted, dtype="long", padding="post", truncating="post", value=tag2idx["O"])
        sentence_tags_test_converted = [[tag2idx[sentence_tag] for sentence_tag in sentence_tags] for sentence_tags in sentences_tags_test]
        sentence_tags_test_padded = pad_sequences(maxlen=max_len, sequences=sentence_tags_test_converted, dtype="long", padding="post", truncating="post", value=tag2idx["O"])

        attention_masks_train = [[float(i>0) for i in ii] for ii in sentence_words_train_padded]
        attention_masks_test = [[float(i>0) for i in ii] for ii in sentence_words_test_padded]

        torch_input_train = torch.LongTensor(sentence_words_train_padded)
        torch_input_test = torch.LongTensor(sentence_words_test_padded)
        torch_tag_train = torch.LongTensor(sentence_tags_train_padded)
        torch_tag_test = torch.LongTensor(sentence_tags_test_padded)
        torch_mask_train = torch.LongTensor(attention_masks_train)
        torch_mask_test = torch.LongTensor(attention_masks_test)

        train_data = TensorDataset(torch_input_train, torch_mask_train, torch_tag_train)
        train_sampler = RandomSampler(train_data)
        train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

        test_data = TensorDataset(torch_input_test, torch_mask_test, torch_tag_test)
        test_sampler = SequentialSampler(test_data)
        test_dataloader = DataLoader(test_data, sampler=test_sampler, batch_size=batch_size)

        if option == 1:
                model = BertForTokenClassification.from_pretrained("bert-base-multilingual-cased", num_labels=len(tag2idx))
                model.cuda()

                FULL_FINETUNING = True
                if FULL_FINETUNING:
                        param_optimizer = list(model.named_parameters())
                        no_decay = ['bias', 'gamma', 'beta']
                        optimizer_grouped_parameters = [
                                {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
                                'weight_decay_rate': 0.01},
                                {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
                                'weight_decay_rate': 0.0}
                        ]
                else:
                        param_optimizer = list(model.classifier.named_parameters()) 
                        optimizer_grouped_parameters = [{"params": [p for n, p in param_optimizer]}]

                optimizer = Adam(optimizer_grouped_parameters, lr=3e-5)
                train_bert(device, model, train_dataloader, optimizer)

        elif option == 2:
                #model = BertForTokenClassification.from_pretrained(models_path)
                config = BertConfig.from_json_file(output_config_file)
                model = BertForTokenClassification(config)
                state_dict = torch.load(output_model_file)
                model.load_state_dict(state_dict)
                test_bert(device, model, test_dataloader)
        


def train_bert(device, model, train_dataloader, optimizer):
        epochs = 5
        max_grad_norm = 1.0

        for _ in trange(epochs, desc="Epoch"):
                # TRAIN loop
                model.train()
                tr_loss = 0
                nb_tr_examples, nb_tr_steps = 0, 0
                for step, batch in enumerate(train_dataloader):
                        # add batch to gpu
                        batch = tuple(t.to(device) for t in batch)
                        b_input_ids, b_input_mask, b_labels = batch
                        # forward pass
                        loss = model(b_input_ids, token_type_ids=None,
                                attention_mask=b_input_mask, labels=b_labels)
                        # backward pass
                        loss.backward()
                        # track train loss
                        tr_loss += loss.item()
                        nb_tr_examples += b_input_ids.size(0)
                        nb_tr_steps += 1
                        # gradient clipping
                        torch.nn.utils.clip_grad_norm_(parameters=model.parameters(), max_norm=max_grad_norm)
                        # update parameters
                        optimizer.step()
                        model.zero_grad()
                # print train loss per epoch
                print("Train loss: {}".format(tr_loss/nb_tr_steps))

        model_to_save = model.module if hasattr(model, 'module') else model

        #output_model_file = os.path.join(models_path, WEIGHTS_NAME)
        #output_config_file = os.path.join(models_path, CONFIG_NAME)

        torch.save(model_to_save.state_dict(), output_model_file)
        model_to_save.config.to_json_file(output_config_file)
        
def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=2).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

def test_bert(device, model, test_dataloader):
        model.eval()
        predictions = []
        true_labels = []
        eval_loss, eval_accuracy = 0, 0
        nb_eval_steps, nb_eval_examples = 0, 0
        for batch in test_dataloader:
                batch = tuple(t.to(device) for t in batch)
                b_input_ids, b_input_mask, b_labels = batch

                with torch.no_grad():
                        tmp_eval_loss = model(b_input_ids, token_type_ids=None,
                                        attention_mask=b_input_mask, labels=b_labels)
                        logits = model(b_input_ids, token_type_ids=None,
                                attention_mask=b_input_mask)
                
                logits = logits.detach().cpu().numpy()
                predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
                label_ids = b_labels.to('cpu').numpy()
                true_labels.append(label_ids)
                tmp_eval_accuracy = flat_accuracy(logits, label_ids)

                eval_loss += tmp_eval_loss.mean().item()
                eval_accuracy += tmp_eval_accuracy

                nb_eval_examples += b_input_ids.size(0)
                nb_eval_steps += 1

        print(true_labels)
        '''
        pred_tags = [[tags_vals[p_i] for p_i in p] for p in predictions]
        valid_tags = [[tags_vals[l_ii] for l_ii in l_i] for l in true_labels for l_i in l ]
        print("Validation loss: {}".format(eval_loss/nb_eval_steps))
        print("Validation Accuracy: {}".format(eval_accuracy/nb_eval_steps))
        print("Validation F1-Score: {}".format(f1_score(pred_tags, valid_tags)))
        '''
        

if __name__ == "__main__":
        startProgram()



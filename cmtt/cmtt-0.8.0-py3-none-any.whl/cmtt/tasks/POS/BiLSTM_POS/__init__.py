from pathlib import Path
import torch
import torch.nn as nn
import os
import dill
from cmtt.preprocessing import *
from cmtt.data.downloader import download_file_from_google_drive

# Training Colab
# https://colab.research.google.com/drive/1mPJCkXroReuPTb3XP0uTByy1TI5vTBc4#scrollTo=JX9dYDOhpwmy

model_files = [
    {   
        'id': "1-AlQ3ivd9DKZqqUKllQTOV6jnbaT0Msg",
        'fname': "TEXT.Field", 
    },
    {   
        'id': "1-JVkPqUT6X77p37OVRb2awZZrAURVPHc",
        'fname': "LABEL.Field", 
    },
    {   
        'id': "1-24TtQiQ4wMOpY-aVO2GHIJQ4BiKqBnO",
        'fname': "pos_model.pt", 
    }
]

path = Path(__file__).parent

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class BiLSTM_MODEL(nn.Module):
    def __init__(self, 
                 input_dim, 
                 embedding_dim, 
                 hidden_dim, 
                 output_dim, 
                 n_layers, 
                 bidirectional, 
                 dropout, 
                 pad_idx):
        
        super().__init__()
        
        self.embedding = nn.Embedding(input_dim, embedding_dim, padding_idx = pad_idx)
        
        self.lstm = nn.LSTM(embedding_dim, 
                            hidden_dim, 
                            num_layers = n_layers, 
                            bidirectional = bidirectional,
                            dropout = dropout if n_layers > 1 else 0)
        
        self.fc = nn.Linear(hidden_dim * 2 if bidirectional else hidden_dim, output_dim)
        
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, text):
        embedded = self.dropout(self.embedding(text))
        outputs, (hidden, cell) = self.lstm(embedded)
        predictions = self.fc(self.dropout(outputs))
        return predictions


class BiLSTM_POS():

    def __init__(self):

        dest = path/'models/'
        if not (dest).exists(): 
            os.makedirs(dest, exist_ok=True)
            print("Downloading model files..")
            for i in model_files:
                download_file_from_google_drive(i['id'], str(dest)+"/"+str(i['fname']), i['fname'], "")
            print("Files downloaded")

        with open(os.path.join(path/'models', "TEXT.Field"),"rb")as f:
            self.TEXT=dill.load(f)

        with open(os.path.join(path/'models', "LABEL.Field"),"rb")as f:
            self.LABEL=dill.load(f)

        INPUT_DIM = len(self.TEXT.vocab)
        EMBEDDING_DIM = 100
        HIDDEN_DIM = 128
        OUTPUT_DIM = len(self.LABEL.vocab)
        N_LAYERS = 2
        BIDIRECTIONAL = True
        DROPOUT = 0.25
        PAD_IDX = self.TEXT.vocab.stoi[self.TEXT.pad_token]

        self.model = BiLSTM_MODEL(INPUT_DIM, 
                                EMBEDDING_DIM, 
                                HIDDEN_DIM, 
                                OUTPUT_DIM, 
                                N_LAYERS, 
                                BIDIRECTIONAL, 
                                DROPOUT, 
                                PAD_IDX)

        pretrained_embeddings = self.TEXT.vocab.vectors

        self.model.embedding.weight.data[PAD_IDX] = torch.zeros(EMBEDDING_DIM)

        self.model = self.model.to(device)

        self.model.load_state_dict(torch.load(os.path.join(path/'models', "pos_model.pt"), map_location=torch.device('cpu')))

    def tag_sentence(self, device, sentence, text_field, tag_field):
        self.model.eval()
        if isinstance(sentence, str):
            # nlp = spacy.load('en_core_web_sm')
            WordT = WordTokenizer()
            tokenized = WordT.tokenize(sentence)
            tokens = []
            for i in tokenized:
                if len(i) != 1 or (len(i) == 1 and not WordT._is_punctuation(i)): 
                    tokens.append(i)             

            # tokens = [token.text for token in nlp(sentence)]
        else:
            tokens = [token for token in sentence]

        if text_field.lower:
            tokens = [t.lower() for t in tokens]
            
        numericalized_tokens = [text_field.vocab.stoi[t] for t in tokens]
        unk_idx = text_field.vocab.stoi[text_field.unk_token]
        unks = [t for t, n in zip(tokens, numericalized_tokens) if n == unk_idx]
        token_tensor = torch.LongTensor(numericalized_tokens)
        token_tensor = token_tensor.unsqueeze(-1).to(device)
        predictions = self.model(token_tensor)
        top_predictions = predictions.argmax(-1)
        predicted_tags = [tag_field.vocab.itos[t.item()] for t in top_predictions]
        return tokens, predicted_tags, unks

    def getPOSTags(self, sentence):
        tokens, predicted_tags, unks = self.tag_sentence(device, sentence, self.TEXT, self.LABEL)
        tuple_list = []
        for i in range(len(tokens)):
            tuple_list.append((tokens[i], predicted_tags[i]))

        return tuple_list

    def getUnks(self, sentence):
        tokens, predicted_tags, unks = self.tag_sentence(device, sentence, self.TEXT, self.LABEL)
        return unks


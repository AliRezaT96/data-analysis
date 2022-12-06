from embeddings import embedding
from transformers import BertTokenizer, BertModel
import fasttext

ft = fasttext.load_model('cc.fa.300.bin')
tokenizer = BertTokenizer.from_pretrained('HooshvareLab/bert-base-parsbert-uncased')
bert_model = BertModel.from_pretrained('HooshvareLab/bert-base-parsbert-uncased', 
                                        output_hidden_states = True  # Whether the model returns all hidden-states.
                                        )
while(True):
    text = input('Enter text: ')
    model = input('Enter model_name: ')
    embedding(model, text, tokenizer, ft, bert_model)
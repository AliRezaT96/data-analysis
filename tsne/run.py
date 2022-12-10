import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import fasttext
from transformers import BertTokenizer, BertModel
from tsne import bert_plot_embeddings, fasttext_plot_embeddings, tfidf_plot_embeddings

data = pd.read_json('/content/attributes.json')

tokenizer = BertTokenizer.from_pretrained('HooshvareLab/bert-base-parsbert-uncased')
bert_model = BertModel.from_pretrained('HooshvareLab/bert-base-parsbert-uncased',
                            output_hidden_states = True # Whether the model returns all hidden-states.
                            )

ft_model = fasttext.load_model('cc.fa.300.bin')

tfidf_vectorizer = TfidfVectorizer()

for attr in data.columns.values:
    all_attrs = []
    for i in range(len(data[attr]['all'])):
        all_attrs.append(data[attr]['all'][i][0])
        if len(data[attr]['all'][i]) >1:
            for j in range(1, len(data[attr]['all'][i])):
                all_attrs.append(data[attr]['all'][i][j])

    bert_plot_embeddings(value=all_attrs, attr=attr, bert_model=bert_model, tokenizer=tokenizer)
    fasttext_plot_embeddings(value=all_attrs, attr=attr, ft=ft_model)
    tfidf_plot_embeddings(value=all_attrs, attr=attr, vectorizer=tfidf_vectorizer)

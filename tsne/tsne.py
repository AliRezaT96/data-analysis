import torch
import plotly.offline as py
import plotly.graph_objs as go
from sklearn.manifold import TSNE

def bert_plot_embeddings(value, attr, bert_model, tokenizer):

    model = bert_model
    model.eval()

    vecs = []
    for i in range(len(value)):
        marked_text = "[CLS] " + value[i] + " [SEP]"

        tokenized_text = tokenizer.tokenize(marked_text)
        indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

        segments_ids = [1] * len(tokenized_text)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])


        with torch.no_grad():

            outputs = model(tokens_tensor, segments_tensors)
            hidden_states = outputs[2]

        token_embeddings = torch.stack(hidden_states, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        
        token_vecs = hidden_states[-2][0]

        # Calculate the average of all 22 token vectors.
        text_embedding = torch.mean(token_vecs, dim=0)
        # vecs.append(tokenizer(value[i], padding='max_length', max_length=512)['input_ids'])
        vecs.append(text_embedding.numpy())

    tsne = TSNE(n_components=2, verbose=1, perplexity=30, n_iter=20000)
    results = tsne.fit_transform(vecs)


    plots = []
    for i in range(len(value)):
        pl = go.Scatter(x=[results[i, 0]], y=[results[i, 1]], mode='markers+text',text=[value[i]],
                        textposition='bottom center',marker=dict(size=10, color=i, colorscale='Jet', opacity=0.8), 
                        textfont=dict(size=14,),name=value[i])
        plots.append(pl)
        
    py.plot(plots, filename=f'bert_embedding_{attr}.html', auto_open=True)

def fasttext_plot_embeddings(value, attr, ft):
    vecs = []

    for w in value:
        vecs.append(ft.get_word_vector(w))

    tsne = TSNE(n_components=2, verbose=1, perplexity=30, n_iter=20000)
    results = tsne.fit_transform(vecs)


    plots = []
    for i in range(len(value)):
        pl = go.Scatter(x=[results[i, 0]], y=[results[i, 1]], mode='markers+text',text=[value[i]],
                        textposition='bottom center',marker=dict(size=10, color=i, colorscale='Jet', opacity=0.8), 
                        textfont=dict(size=14,),name=value[i])
        plots.append(pl)
        
    py.plot(plots, filename=f'fasttext_embedding_{attr}.html', auto_open=True)


def tfidf_plot_embeddings(value, attr, vectorizer):
    X = vectorizer.fit_transform(value)

    tsne = TSNE(n_components=2, verbose=1, perplexity=30, n_iter=20000)
    results = tsne.fit_transform(X)


    plots = []
    for i in range(len(value)):
        pl = go.Scatter(x=[results[i, 0]], y=[results[i, 1]], mode='markers+text',text=[value[i]],
                        textposition='bottom center',marker=dict(size=10, color=i, colorscale='Jet', opacity=0.8), 
                        textfont=dict(size=14,),name=value[i])
        plots.append(pl)
        
    py.plot(plots, filename=f'tfidf_embedding_{attr}.html', auto_open=True)
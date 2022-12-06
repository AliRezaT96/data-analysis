import torch


def embedding(model_name, text, tokenizer, ft, bert_model):
    if model_name == 'bert' or model_name == 'Bert' or model_name == 'BERT':

        marked_text = "[CLS] " + text + " [SEP]"

        tokenized_text = tokenizer.tokenize(marked_text)
        indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

        segments_ids = [1] * len(tokenized_text)

        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])
        
        model = bert_model
        # model = BertModel.from_pretrained('HooshvareLab/bert-base-parsbert-uncased',
        #                           output_hidden_states = True, # Whether the model returns all hidden-states.
        #                           )

        # Put the model in "evaluation" mode, meaning feed-forward operation.
        model.eval()

        with torch.no_grad():

            outputs = model(tokens_tensor, segments_tensors)
            hidden_states = outputs[2]

        token_embeddings = torch.stack(hidden_states, dim=0)
        token_embeddings = torch.squeeze(token_embeddings, dim=1)
        
        token_vecs = hidden_states[-2][0]

        # Calculate the average of all 22 token vectors.
        text_embedding = torch.mean(token_vecs, dim=0)

        print(f"tokenized text: {tokenized_text}\n")

        print(f'text vector: {text_embedding}\n')


    elif model_name == 'fasttext' or model_name == 'fastext' or model_name == 'fast':
        vector = ft.get_word_vector(text)

        print(f'vector of {text}:\n', vector)
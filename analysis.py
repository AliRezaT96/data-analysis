import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
from collections import defaultdict
import matplotlib.pyplot as plt

def num_val_for_attr(df):
    attributes = pd.unique(df.attribute)
    attribute_counts = {}
    
    for attr in attributes:
        count = 0
        for i in range(len(df)):
            if df.attribute[i] == attr:
                count+=1
                
        attribute_counts[attr] = count

    return attribute_counts

def text_reshaper(text):
    att_list = []
    for i in range(len(text)):
        reshaped = arabic_reshaper.reshape(text[i])
        att_list.append(get_display(reshaped))
    
    return att_list

def NgramsValue(df, n): # n --> 2: bigram, 3: trigram
    Values = defaultdict(int)
    for text in df.caption:
        for word in generate_N_grams(text,n):
            Values[word]+=1
    df_values = pd.DataFrame(sorted(Values.items(),key=lambda x:x[1],reverse=True))

    return df_values


def generate_N_grams(text,ngram):
    words=[word for word in text.split(" ")]
    temp=zip(*[words[i:] for i in range(0,ngram)])
    ans=[' '.join(ngram) for ngram in temp]
    return ans
    

def plot_Ngrams(ngram_text, ngram_num, ngram):
    plt.xticks(rotation='vertical')
    plt.figure(1,figsize=(16,4))
    plt.bar(ngram_text, ngram_num, color ='blue',
            width = 0.4)
    plt.xlabel("Words")
    plt.ylabel("Count")
    plt.title("Top 20 words")
    plt.savefig(f'{ngram}.jpg')
    fig = plt.show()
    return fig
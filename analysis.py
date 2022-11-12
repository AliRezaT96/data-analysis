import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from wordcloud_fa import WordCloudFa
import yaml
from yaml.loader import SafeLoader
import re
import seaborn as sns
sns.set()

from data import read_data


with open('config.yaml',encoding='utf8') as f:
    opt = yaml.load(f, SafeLoader)

df = read_data(opt['data'])
df_ner = read_data(opt['data_ner'])




def wordcloud(counter, name):
    wc = WordCloudFa(width=1200, height=800, 
                   background_color="white", 
                   max_words=200) 
    wc.generate_from_frequencies(counter)

    # Plot
    fig=plt.figure(figsize=(6, 4))
    plt.title(f'word cloud for {name}')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig(f"{get_display(arabic_reshaper.reshape(name))}'s word cloud.jpg")
    plt.show()


def common_words(attr1, attr2):

    attribute1 = list(df[df['attribute']==attr1].value.values)
    attribute2 = list(df[df['attribute']==attr2].value.values)

    common = []
    for i in range(len(attribute1)):
        for j in range(len(attribute2)):
            if attribute1[i] == attribute2[j]:
                common.append(attribute1[i])
    plt.show(wordcloud(Counter(common), get_display(arabic_reshaper.reshape(f"اشتراک {attr1} و {attr2}"))))


def common_words_no_attr():
    captions = list(df_ner['caption'])
    for i in range(len(df_ner['value'])):
        for val in df_ner['value'][i].split(','):
            captions[i] = re.sub(val, '', captions[i])
    
    all_captions = []
    for i in range(len(captions)):
        all_captions.extend(captions[i].split())
    wordcloud(Counter(all_captions), get_display(arabic_reshaper.reshape('کلمات مشترک بدون ویژگی')))


def text_reshaper(text):
    att_list = []
    for i in range(len(text)):
        att_list.append(get_display(arabic_reshaper.reshape(text[i])))
    
    return att_list


def my_tokenizer(text):
    return text.split() if text != None else []


def multi_boxplot(data, x, y, ylim = None):
    '''Wrapper for sns boxplot with cut-off functionality'''
    # plt.figure(figsize=(30, 5))
    fig, ax = plt.subplots()
    plt.xticks(rotation=90) 

    # order boxplots by median
    ordered_values = data.groupby(x)[[y]] \
                         .median() \
                         .sort_values(y, ascending=False) \
                         .index
        
    sns.boxplot(x=x, y=y, data=data, palette='Set2', 
                order=ordered_values)

    fig.set_size_inches(11, 6)
    
    # cut-off y-axis at value ylim
    ax.set_ylim(0, ylim)

    plt.savefig('token distribution per attribute.jpg')


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
    plt.show()


class Analysis():
    def __init__(self, df):
        self.data = df
        self.attributes = pd.unique(self.data.attribute)
    
    def plot_value_per_attribute(self):
        plt.xticks(rotation='vertical')
        plt.bar(text_reshaper(list(self.attributes)), self.data.attribute.value_counts())
        plt.savefig('value per attribute.jpg')
        plt.show()
    
    def plot_word_count(self):
        self.data.words_count.plot(kind='hist')

    def word_cloud(self):
        # most common words in each attribute
        def most_common(counter, attr):
            freq_df = pd.DataFrame.from_records(counter.most_common(20), columns=['token', 'count'])
            freq_df.plot(kind='bar', x='token')
            plt.title(f'{get_display(arabic_reshaper.reshape(attr))} most common')
            plt.savefig(f'{attr} most common words.jpg')
            plt.show()

        for attr in self.attributes:
            attr_df = self.data[self.data['attribute'] == attr]
            tokens = attr_df.value
            counter = Counter(tokens)
            wordcloud(counter, get_display(arabic_reshaper.reshape(attr)))
            most_common(Counter(text_reshaper(list(tokens))), attr)


    # this shows which attribute has more token in all captions
    def mean_number_of_tokens(self):
        self.data.groupby(['attribute']).agg({'words_count':'mean'}).sort_values(by='words_count', ascending=False).plot(kind='bar', figsize=(7,4))
        plt.savefig('mean number of tokens.jpg')


    def TokenDestribution(self):
        multi_boxplot(self.data, 'attribute', 'words_count')

    def NgramsValue(self): # n --> 2: bigram, 3: trigram
        BiValues = defaultdict(int)
        TriValues = defaultdict(int)

        for text in self.data.caption:
            for word in generate_N_grams(text, 2):
                BiValues[word]+=1

        bigram_values = pd.DataFrame(sorted(BiValues.items(),key=lambda x:x[1],reverse=True))
        bi_text = text_reshaper(bigram_values[0][:opt['ngram_number']])
        bi_num = bigram_values[1][:opt['ngram_number']]

        plot_Ngrams(bi_text, bi_num, 'bigram')

        for text in self.data.caption:
            for word in generate_N_grams(text, 3):
                TriValues[word]+=1
        
        trigram_values = pd.DataFrame(sorted(TriValues.items(),key=lambda x:x[1],reverse=True))
        tri_text = text_reshaper(trigram_values[0][:opt['ngram_number']])
        tri_num = trigram_values[1][:opt['ngram_number']]
        plot_Ngrams(tri_text, tri_num, 'trigram')


analize_text = Analysis(df)
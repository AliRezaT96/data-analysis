import pandas as pd
from analysis import num_val_for_attr, generate_N_grams
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
sns.set()

all_captions = []
with open('/data/captions.txt', 'r', encoding='utf-8-sig') as f:
    for line in f:
        all_captions.append(line.strip('\n'))


caption = []
attribute = []
value = []
for i in range(len(all_captions)):
    caption.append(all_captions[i].split('@@@')[0])
    attribute.append(all_captions[i].split('@@@')[1])
    value.append(all_captions[i].split('@@@')[2])

df = pd.DataFrame()
df['caption'] = caption
df['attribute'] = attribute
df['value'] = value

num_words = []
for i in range(len(df)):
    num_words.append(len(df.caption.values[i].split()))

df['number_of_words'] = num_words

data = num_val_for_attr(df)
att_list = []
for i in range(len(data.keys())):
    reshaped = arabic_reshaper.reshape(list(data.keys())[i])
    att_list.append(get_display(reshaped))

# plot distribution of number of words for each caption
sns.displot(data=df, x='words_count', kind='hist', aspect=1.4)
plt.show()


# number of values for each attribute
plt.title('number of values per attribute')
plt.xticks(rotation='vertical')
plt.bar(att_list, data.values())
plt.show()

# bigram
BigramValues=defaultdict(int)
for text in df.caption:
    for word in generate_N_grams(text,2):
        BigramValues[word]+=1

df_values2gram = pd.DataFrame(sorted(BigramValues.items(),key=lambda x:x[1],reverse=True))

# for showing more or less number of words, change range number:
bi1=df_values2gram[0][:20]
bi2=df_values2gram[1][:20]

bigram = []
for i in range(len(bi1)):
    reshaped = arabic_reshaper.reshape(bi1[i])
    bigram.append(get_display(reshaped))


plt.xticks(rotation='vertical')
plt.figure(1,figsize=(16,4))
plt.bar(bigram,bi2, color ='blue',
        width = 0.4)
plt.xlabel("Words")
plt.ylabel("Count")
plt.title("Bigram: Top 20 words")
plt.show()


# trigram
TrigramValues=defaultdict(int)
for text in df.caption:
    for word in generate_N_grams(text,3):
        TrigramValues[word]+=1

df_values3gram = pd.DataFrame(sorted(TrigramValues.items(),key=lambda x:x[1],reverse=True))

# for showing more or less number of words, change range number:
ti1=df_values3gram[0][:20]
ti2=df_values3gram[1][:20]


trigram = []
for i in range(len(ti1)):
    reshaped = arabic_reshaper.reshape(ti1[i])
    trigram.append(get_display(reshaped))


# In[165]:


plt.xticks(rotation='vertical')
plt.figure(1,figsize=(16,4))
plt.bar(trigram,ti2, color ='blue',
        width = 0.4)
plt.xlabel("Words")
plt.ylabel("Count")
plt.title("Trigram: Top 20 words")
plt.show()

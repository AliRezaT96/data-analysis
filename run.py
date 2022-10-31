import pandas as pd
from analysis import num_val_for_attr, generate_N_grams, text_reshaper, NgramsValue, plot_Ngrams
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
from collections import defaultdict
import seaborn as sns
sns.set()

# loading data
all_captions = []
with open('/data/captions.txt', 'r', encoding='utf-8-sig') as f:
    for line in f:
        all_captions.append(line.strip('\n'))


# seperate caption, attribute and value
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


# number of words for each caption
num_words = []
for i in range(len(df)):
    num_words.append(len(df.caption.values[i].split()))

df['words_count'] = num_words

# plot distribution of number of words for each caption
sns.displot(data=df, x='words_count', kind='hist', aspect=1.4)
plt.savefig('words_count.jpg')
plt.show()


# number of values for each attribute
attribute_count = num_val_for_attr(df) # attribute count dict
reshaped_attr_list = text_reshaper(list(attribute_count.keys())) # reshape attribute to show properly in plot


plt.title('number of values per attribute')
plt.xticks(rotation='vertical')
plt.bar(reshaped_attr_list, attribute_count.values())
plt.savefig('number of values')
plt.show()

# bigram
df_values2gram = NgramsValue(df, 2)

# for showing more or less number of words, change range number:
bi_text=df_values2gram[0][:20]
bi_num=df_values2gram[1][:20]

bigram = text_reshaper(bi_text)

print(plot_Ngrams(bigram, bi_num, 'bigram'))

# trigram
df_values3gram = NgramsValue(df, 3)

# for showing more or less number of words, change range number:
ti_text=df_values3gram[0][:20]
ti_num=df_values3gram[1][:20]

trigram = text_reshaper(ti_text)

print(plot_Ngrams(trigram, ti_num, 'trigram'))

import pandas as pd


def read_data(path):
    all_captions = []
    with open(path, 'r', encoding='utf-8-sig') as f:
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
    
    return df
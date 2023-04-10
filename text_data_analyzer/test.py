import pandas as pd
import numpy as np
import json
# from analysis import empty_hashtag
from analysis import analysis

import matplotlib.pyplot as plt

import streamlit as st

def display(posts, products):
    st.title("Text Analysis")

    analyze = analysis(posts=posts, products=products)

    text = st.selectbox('select option', ['hashtags',
                                          'nlp_output'
                                          ])
    
    if text == "hashtags":
        pass
        empty_caption_count, hashtag_beginning, empty_caption_before_hashtag, number_product_all_captions, number_product_start_with_hashtag, number_product_without_hashtag = analyze.empty_hashtag()
        
        st.title('empty captions and hashtags')
        st.success("number of empty captions: {}".format(empty_caption_count))
        st.success("number of captions with hashtags at the beginning: {}".format(hashtag_beginning))
        st.success("number of empty caption before hashtag: {}".format(empty_caption_before_hashtag))

        captions = {"empty_caption_count":  empty_caption_count,
                           "hashtag_beginning": hashtag_beginning,
                           "empty_caption_before_hashtag": empty_caption_before_hashtag
                           }
        
        
        chart = pd.DataFrame(captions, index=[0])
        st.bar_chart(data=chart)

        
        st.title("product in captions")
        st.success("number of products in captions: {}".format(number_product_all_captions))
        st.success("number of product in captions start with hashtag: {}".format(number_product_start_with_hashtag))
        st.success("number of product in captions without hashtag: {}".format(number_product_without_hashtag))

        pros_in_caption = {"number_product_all_captions":  number_product_all_captions,
                           "number_product_start_with_hashtag": number_product_start_with_hashtag,
                           "number_product_without_hashtag": number_product_without_hashtag
                           }
        
        
        chart = pd.DataFrame(pros_in_caption, index=[0])
        st.bar_chart(data=chart)


    elif text == "nlp_output":
        no_product_name, product_count_before_cleaning, product_count_after_cleaning, empty_caption, pro_in_hashtag_count, texture_count, model_count, gender_count, style_count, posts_with_pro_count, no_texture_count, no_model_count, no_gender_count, no_style_count = analyze.nlp_out()
        # st.success("attribute(categories) counts:\n texture:{}\n model:{}\n gender:{}\n style:{}\n".format(texture_count, model_count, gender_count, style_count))
        st.title('attribute count')
        st.success("number of categories in nlp out for {} posts".format(len(posts)))
        categories_dict = {"texture_count":  texture_count,
                           "model_count": model_count,
                           "gender_count": gender_count,
                           "style_count": style_count
                           }
        fig = plt.figure(figsize=(10, 5))
        plt.xticks(rotation='vertical')
        plt.bar(list(categories_dict.keys()), list(categories_dict.values()))
        st.pyplot(fig)


        st.title('no attribute')
        st.success("number of categories in nlp out for {} posts".format(len(posts)))
        no_categories_dict = {"texture_count":  no_texture_count,
                           "model_count": no_model_count,
                           "gender_count": no_gender_count,
                           "style_count": no_style_count
                           }
        fig = plt.figure(figsize=(10, 5))
        plt.xticks(rotation='vertical')
        plt.bar(list(no_categories_dict.keys()), list(no_categories_dict.values()))
        st.pyplot(fig)

        st.title('no product name')
        st.success("number of posts with no product name: {}".format(no_product_name))
        st.success("number of empty captions that dont have product name: {}".format(empty_caption))
        no_pro_name = {"all":len(posts),
                       "no_product_name":  no_product_name,
                       "empty_caption": empty_caption}
        

        chart = pd.DataFrame(no_pro_name, index=[0])
        st.bar_chart(data=chart)

        st.title('product in captions before and after cleaning')
        st.success("number of products before cleaning: {}".format(product_count_before_cleaning))
        st.success("number of products after cleaning: {}".format(product_count_after_cleaning))
        
        pro_in_caption = {"product_count_before_cleaning":  product_count_before_cleaning,
                       "product_count_after_cleaning": product_count_after_cleaning}
        

        chart = pd.DataFrame(pro_in_caption, index=[0])
        st.bar_chart(data=chart)


        st.title('product in hashtags')
        st.success("number of product in hashtag: {}".format(pro_in_hashtag_count))
        
        pro_in_hashtag = {"pro_in_hashtag_count":  pro_in_hashtag_count,
                       "posts_with_product_name": posts_with_pro_count}
        

        chart = pd.DataFrame(pro_in_hashtag, index=[0])
        st.bar_chart(data=chart)







# data = json.load(open("C:/Users/Ali/Desktop/RandomSamplesFromInstagram_Data_Main.json", encoding="utf-8-sig"))
data = json.load(open("C:/Users/Ali/Desktop/nlp_out.json", encoding="utf-8-sig"))
posts = pd.DataFrame(data[:1000])

classes = json.load(open("D:/label_studio_segmentation/class_ls.json", encoding="utf-8-sig"))
pros = list(classes['product'].values())[:-1]
products = pros[0]

for i in range(len(pros[1:])):
    products.extend(pros[i])

display(posts, products)
# analyze = analysis(posts=posts, products=products)
# empty_caption_count, hashtag_beginning, empty_caption_before_hashtag, number_product_all_captions, number_product_start_with_hashtag, number_product_without_hashtag = aalyze.empty_hashtag()

# no_product_name, product_count_before_cleaning, product_count_after_cleaning, empty_caption, pro_in_hashtag_count, texture_count, model_count, gender_count, style_count = analyze.nlp_out()


# empty_caption_id, hashtag_beginning_id, empty_caption_before_hashtag_id = empty_hashtag(posts, products)

# print("#############\n", len(empty_caption_id), len(hashtag_beginning_id), len(empty_caption_before_hashtag_id))

########################################################################################

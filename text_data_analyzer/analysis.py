import pandas as pd
import numpy as np
import json

from cleaner import cleaning
class analysis:
    def __init__(self, posts, products) -> None:
        self.posts = posts
        self.products = products

        # hashtags
        self.empty_caption_count = 0
        self.hashtag_beginning = 0
        self.empty_caption_before_hashtag = 0   # after cleaning

        # nlp output
        self.no_product_name = 0
        self.texture_count, self.model_count, self.gender_count, self.style_count = 0, 0, 0, 0
        self.empty_caption_nlp_out = 0
        self.product_count_before_cleaning = 0
        self.product_count_after_cleaning = 0
        self.pro_in_hashtag_count = 0


    def empty_hashtag(self):

        def pro_in_text(_post):
            number_of_product_in_caption = 0
            for i in range(len(_post)):
                for pro in self.products:
                    if pro in _post.loc[i]['caption']:
                        number_of_product_in_caption += 1
                        break
            return number_of_product_in_caption
            
        empty_caption_id, hashtag_beginning_id, empty_caption_before_hashtag_id = [], [], []
        
        for i in range(len(self.posts)):
            if self.posts.loc[i]['caption'] == '':
                self.empty_caption_count += 1
                empty_caption_id.append(self.posts.loc[i]["_id"])

            elif self.posts.loc[i]["caption"][0] == '#':
                self.hashtag_beginning += 1
                hashtag_beginning_id.append(self.posts.loc[i]["_id"])
            else:
                for j in range(len(self.posts.loc[i]["caption"])):
                    if self.posts.loc[i]["caption"][j] == "#" and len(self.posts.loc[i]["caption"][:j]) > 0:
                        text_before_hashtag = cleaning(self.posts.loc[i]["caption"][:j])
                        if len(text_before_hashtag) == 0:
                            self.empty_caption_before_hashtag += 1
                            empty_caption_before_hashtag_id.append(self.posts.loc[i]["_id"])
                            break
        
        # print("empty caption count: {}".format(empty_caption_count))
        # print("\nhashtag at the beginning count: {}".format(hashtag_beginning))
        # print("\nempty caption before hashtag count: {}".format(empty_caption_before_hashtag))

        ############# product in caption ##########
        post = self.posts[self.posts._id.isin(empty_caption_id) == False].reset_index(drop=True) # deleted empty captions from posts
        number_product_all_captions = pro_in_text(post)
        # print("number of product in all captions: {}".format(number_product_all_captions))

        posts_without_hashtags_in_beginning = post[post._id.isin(hashtag_beginning_id) == False].reset_index(drop=True)
        number_product_start_with_hashtag = pro_in_text(posts_without_hashtags_in_beginning)
        # print("\nnumber of product in captions that dont starts with hashtag: {}".format(number_product_start_with_hashtag))

        cleaned_posts = posts_without_hashtags_in_beginning[post._id.isin(empty_caption_before_hashtag_id) == False].reset_index(drop=True)
        number_product_without_hashtag = pro_in_text(cleaned_posts)
        # print("\nnumber of product in captions without hashtag: {}\n".format(number_product_without_hashtag))

        return self.empty_caption_count, self.hashtag_beginning, self.empty_caption_before_hashtag, number_product_all_captions, number_product_start_with_hashtag, number_product_without_hashtag



    ############# nlp output ##################
    def nlp_out(self):
        # no_product_name = 0
        no_texture_count, no_model_count, no_gender_count, no_style_count = 0, 0, 0, 0
        no_product_id = []
        for i in range(len(self.posts)):
            # texture_count
            if self.posts.loc[i]['nlp_output'][0]["texture"][0]['token'] != "":
                self.texture_count += len(self.posts.loc[i]['nlp_output'][0]["texture"][0]['category'])
            else:
                no_texture_count += 1
            
            # model_count
            if self.posts.loc[i]['nlp_output'][0]["model"][0]['token'] != "":
                self.model_count += len(self.posts.loc[i]['nlp_output'][0]["model"][0]['category'])
            else:
                no_model_count += 1

            # gender_count
            if self.posts.loc[i]['nlp_output'][0]["gender"][0]['token'] != "":
                self.gender_count += len(self.posts.loc[i]['nlp_output'][0]["gender"][0]['category'])
            else:
                no_gender_count += 1
            
            # style_count
            if self.posts.loc[i]['nlp_output'][0]["style"][0]['token'] != "":
                self.style_count += len(self.posts.loc[i]['nlp_output'][0]["style"][0]['category'])
            else:
                no_style_count += 1

            # no product name
            if self.posts.loc[i]['nlp_output'][0]['product_name'] == []:
                self.no_product_name += 1
                no_product_id.append(self.posts.loc[i]['_id'])
        # print("number of empty product name in nlp output: {}".format(no_product_name))

        # product_count_before_cleaning = 0
        # product_count_after_cleaning = 0
        # empty_caption = 0
        for _id in no_product_id:
            for i in range(len(self.posts)):
                if _id == self.posts.loc[i]['_id']:
                    if self.posts.loc[i]['caption'] == "":
                        self.empty_caption_nlp_out += 1
                    else:
                        for pro in self.products:
                            if pro in self.posts.loc[i]['caption']:
                                self.product_count_before_cleaning += 1
                                
                        text = cleaning(self.posts.loc[i]['caption'])
                        for pro in self.products:
                            if pro in text:
                                self.product_count_after_cleaning += 1
                                break
        # print("number of product in empty product name after cleaning: {}".format(product_count_after_cleaning))
        # print("number of product in empty product name before cleaning: {}".format(product_count_before_cleaning))
        # print("number of empty caption in empty product name: {} of {} posts".format(empty_caption_for_product, len(self.posts)))

        posts_with_pro = []
        posts_with_pro = self.posts[self.posts._id.isin(no_product_id) == False].reset_index(drop=True)
        # for i in range(len(self.posts)):
        #     if self.posts.loc[i]["_id"] not in no_product_id:
        #         posts_with_pro.append(self.posts.loc[i])
        # len(posts_with_pro)

        ###
        # pro_in_hashtag_count = 0
        for i in range(len(posts_with_pro)):
            hashtags_list = []
            for text in posts_with_pro.loc[i]['caption'].split('#'):
                for j in range(len(text)):
                    try:
                        if text[j] == " ":
                            hashtags_list.append(text[:j])
                            break
                    except:
                        pass
                    
            for j in range(len(hashtags_list[:5])):
                if posts_with_pro.loc[i]['nlp_output'][0]['product_name'] in hashtags_list[j]:
                    self.pro_in_hashtag_count += 1
                    break
                        
        # print(pro_in_hashtag_count)


        return self.no_product_name, self.product_count_before_cleaning, self.product_count_after_cleaning, self.empty_caption_nlp_out, self.pro_in_hashtag_count, self.texture_count, self.model_count, self.gender_count, self.style_count, len(posts_with_pro), no_texture_count, no_model_count, no_gender_count, no_style_count


    def single_post(self, post):
        if post['nlp_output'][0]["texture"][0]['token'] != "":
            self.texture_count += len(self.posts['nlp_output'][0]["texture"][0]['category'])
        
        # model_count
        if post['nlp_output'][0]["model"][0]['token'] != "":
            self.model_count += len(post['nlp_output'][0]["model"][0]['category'])

        # gender_count
        if post['nlp_output'][0]["gender"][0]['token'] != "":
            self.gender_count += len(post['nlp_output'][0]["gender"][0]['category'])
        
        # style_count
        if post['nlp_output'][0]["style"][0]['token'] != "":
            self.style_count += len(post['nlp_output'][0]["style"][0]['category'])
        
        # no product name
        if post['nlp_output'][0]['product_name'] == []:
            self.no_product_name += 1
    

    # return empty_caption_id, hashtag_beginning_id, empty_caption_before_hashtag_id

    # return empty_caption_count, empty_caption_id, hashtag_beginning, hashtag_beginning_id, empty_caption_before_hashtag, empty_caption_before_hashtag_id

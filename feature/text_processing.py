#!/usr/bin/env python
# coding: utf-8

# In[1]:


def lib():
    global pd, np, spacy, re, nltk, stopwords, nlp
    import pandas as pd
    import numpy as np
    import re
    import spacy
    import nltk
    from nltk.corpus import stopwords
    nlp = spacy.load('en_core_web_sm')


# In[2]:


def text_clean(review):
    def clean(text):
        text = str(text)
        lib()
        # Filter out characters which are not alphabets
        #text = str.replace(text,"n't",'not')
        text = re.sub(r'[^a-zA-Z.\']', ' ',text)
        text = re.sub(r'[\']', '',text)
        text = re.sub(r'[^\x00-\x7F]+','',text)
        text = str.replace(text,'hrs','hours')
        text = str.replace(text,'lappy','laptop')
        text = re.sub("\s\s+", " ", text)
        text = str.replace(text,'loptop','laptop')
        text = str.replace(text,'nyc','nice')
        #text = str.replace(text,'nt','not')
        text = str.replace(text,'warranoty','warranty')
        
        # Coverting to lowercase letters
        text = text.lower()
        return text
    # Applying clean_text function to original reviews
    clean_review = review.apply(lambda text: clean(text))
    return(clean_review)


# In[3]:


def pos(text):
#     text = text_clean(text)
    pos_tags = []
    for i in text:
        doc = nlp(i)
        temp = []
        for token in doc:
            temp.append((token,token.pos_))
        pos_tags.append(temp)
    return(pos_tags)


# In[4]:


def noun(review_tags):
#     review_tags = pos(review_tags)
    nouns = []
    noun_list = []
    for i in range(len(review_tags)):
        temp = []
        for j in range(len(review_tags[i])):
            if review_tags[i][j][1] in ['NOUN','PROPN']:
                temp.append(str(review_tags[i][j][0]))
        nouns.append(temp)
        for i in nouns:
            a = [w for w in i if len(w)>1]
        noun_list.append(a)
    return(noun_list)


# In[5]:


def remove_stopwords(text):
        #word_list = noun(text)
        # List of English stopwords
        eng_stopwords = stopwords.words('english')
        words = []
        for item in text:
            temp = []
            for word in item:
                if word not in eng_stopwords:
                    temp.append(word)
            words.append(temp)
        return(words)


# In[6]:


def cleaned_text(review):
    text=text_clean(review)
    pos_tags=pos(text)
    noun_list=noun(pos_tags)
    cleaned=remove_stopwords(noun_list)
    return(cleaned, text, pos_tags)
    


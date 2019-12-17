#!/usr/bin/env python
# coding: utf-8

# In[1]:


def Opinion(adjective_df):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import pandas as pd
    sid = SentimentIntensityAnalyzer()
    adjective_df['Sentiment_Score'] = adjective_df['Nearest_Adjective'].apply(lambda word: sid.polarity_scores(word)['compound'])
    adjective_df = adjective_df.sort_values(by = 'Feature')
    adjective_df = adjective_df.reset_index(drop = True)
    mapped = pd.read_csv("./feature/Polarity_of_Unidentified_Opinions.csv") 
    a = []
    for i in range(len(mapped)):
        (a.append((mapped.Opinions[i], mapped.Mapped_Opinion[i])))
    adjective_df['New'] = '0'
    for idx,adjective in adjective_df.Nearest_Adjective.items():
        for item in a:
            if item[0] == adjective:
                adjective_df.New[idx] = item[1]
                break

        else:
            adjective_df.New[idx] = adjective_df.Nearest_Adjective[idx]
    adjective_df['New_Score'] = adjective_df['New'].apply(lambda word: sid.polarity_scores(word)['compound'])
    return(adjective_df)


#!/usr/bin/env python
# coding: utf-8

# In[3]:


def feature_matrix1(noun_features,clean_review):
    import pandas as pd
    global pd
    temp = []
    a = [''.join(x) for x in list(noun_features.Consequent)]
    df = pd.DataFrame()
    feature = ''
    conj = ["after", "although"," and", "as", "soon", "because", "before", "both", 
            "but", "either", "even", "for", "how", "however", "if", "neither", "now","the",
            "once", "or", "only", "provided", "rather", "since", "so", "than", "though", "hence", 
            "till", "unless", "until", "when", "whenever", "where", "whereas", "wherever", "whether", "while", "yet","who"]
    for i in range(len(a)):  
        counter = []
        for review in clean_review:
            count=0
            words = review.split()
            if a[i] in words:
                feature = (a[i])
                first = words.index(a[i])
                count=1
            counter.append(count)
        df[feature] = counter
        
    return(df)


# In[4]:


def extract_adjective_1(df,clean_review):
    from feature.text_processing import text_clean
    from nltk.tokenize import sent_tokenize
    import pandas as pd
    import numpy as np
    import spacy
    nlp = spacy.load('en_core_web_sm')
    sent_list = []        
    for j in clean_review:
        sent = sent_tokenize(j)
        sent_list.append(sent)
  
    conj = ["after", "although","and", "as", "soon", "because", "before", "both", 
          "but", "either", "even", "for", "how", "however", "if", "neither", "now","the",
          "once", "or", "only", "provided", "rather", "since", "so", "than", "though", "hence", 
          "till", "unless", "until", "when", "whenever", "where", "whereas", "wherever", "whether", "while", "yet","who"]
    review = {}
    for i in df.columns:
        temp = []
        for sents in sent_list:
            for sent in sents:
                words = sent.split()
                try:
                    if words.index(i):
                        temp.append(sent)
                except:
                    continue
        review[i] = temp

    test=[]
    for k, v in review.items():
        test.append([str(k),str(v)])
    feature_review = pd.DataFrame(test,columns = ['Feature','Reviews'])
    
    #return(feature_review)
    rev_1 = feature_review.Reviews.str.split(',',expand = True)
    #print(rev_1)
    feature_review = pd.concat([feature_review,rev_1],axis=1)
    feature_review = pd.melt(feature_review,id_vars = list(feature_review.columns)[0:2],value_vars=list(feature_review.columns)[2:] ,var_name='Reviews',value_name='Review')
    feature_review.dropna(axis=0,inplace=True)
    feature_review.sort_values(by = 'Feature')
    feature_review.drop(['Reviews'],axis=1,inplace = True)
    feature_review.reset_index(drop=True,inplace=True)
    reviews = feature_review.Review
    def pos1(text):
        text = text_clean(text)
        pos_tags = []
        for i in text:
            doc = nlp(i)
            temp = []
            for token in doc:
                temp.append((token,token.pos_))
            pos_tags.append(temp)
        return(pos_tags)
    pos_tags = pos1(reviews)
  
    adjective = []
  
    for i in range(len(pos_tags)):
        temp = []
        for j in range(len(pos_tags[i])-1):
            if pos_tags[i][j][1] in ['ADJ','ADV'] and pos_tags[i][j+1][1] in ['ADJ']: 
                    temp.append(str(pos_tags[i][j][0])+ ' ' + str(pos_tags[i][j+1][0]))
                    
            if pos_tags[i][j][1] in ['ADV'] and pos_tags[i][j+1][1] == 'VERB': 
                    temp.append(str(pos_tags[i][j][0])+ ' ' + str(pos_tags[i][j+1][0])) 
                        
            if pos_tags[i][j][1] in ['ADJ'] and pos_tags[i][j+1][1] not in ['ADJ','ADV']:
                    if j>1 and pos_tags[i][j-1][1] not in ['ADJ','ADV']:
                        temp.append(str(pos_tags[i][j][0]))
                            
            if pos_tags[i][j+1][1] in ['ADJ'] and pos_tags[i][j][1] not in ['ADJ','ADV']:
                    temp.append(str(pos_tags[i][j+1][0]))
                        
            if pos_tags[i][j+1][1] in ['ADJ'] and str(pos_tags[i][j][0]) in ['not','never']:
                    temp.append(str(pos_tags[i][j][0]) + ' ' + str(pos_tags[i][j+1][0]))

                
        adjective.append(list(np.unique(temp)))
    feature_review['Adjective'] = adjective
    
    nearest_adj = []
    for i in range(len(feature_review)):
        feature = feature_review.Feature[i].strip("()").replace("'",'').split(', ')
      
        sent = feature_review.Review[i]
        sent = sent.replace('.',' ')
      #print(tokens)
        try:
            feature_index1 = sent.index(feature[0])
            #feature_index2 = sent.index(feature[1])
          #print(feature_index1,feature_index2)
            temp = []
            adj = []
            for adjective in feature_review.Adjective[i]:
                adj.append(adjective)
                temp.append(sent.index(adjective))
            diff = []
          #print(temp)
            for j in temp:
                diff.append((abs(feature_index1-j)))
          #print(diff)
            idx = diff.index(min(diff))
            nearest_adj.append(adj[idx])
        except:
            nearest_adj.append('')
            continue
    feature_review['Nearest_Adjective'] = nearest_adj
    return(feature_review)


# In[5]:


def FeatureExtraction(cleaned,text,polarity):
    from feature.feature_creation import association
    from feature.Polarity_Assignment1 import Opinion
    import pandas as pd
    single_f=association(cleaned, min_support=0.03,max_length = 1)
    feature_1=feature_matrix1(single_f,text)
    adj=extract_adjective_1(feature_1,text)
    polarity1=Opinion(adj)
    adjective_df2 = pd.concat([polarity,polarity1],axis=0)
    return(adjective_df2)


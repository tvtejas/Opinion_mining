#!/usr/bin/env python
# coding: utf-8

# In[1]:


def association(text,min_support=0.01,max_length = 2):
    from apyori import apriori
    import pandas as pd
    global pd, apriori
    words=text
#     words = remove_stopwords(text)\
    association_rules = apriori(words, min_support=0.01,max_length = 2)
    association_results = list(association_rules)
    # Creating  Rules Dataframe
    features = pd.DataFrame(columns=('Antecedent','Consequent','Support','Confidence','Lift'))

    support =[]
    confidence = []
    lift = []
    antecedent = []
    consequent=[]

    for record in association_results:
        for ordered_stat in record.ordered_statistics:
            support.append(record.support)
            antecedent.append(ordered_stat.items_base)
            consequent.append(ordered_stat.items_add)
            confidence.append(ordered_stat.confidence)
            lift.append(ordered_stat.lift)

    features['Antecedent'] = antecedent
    features['Consequent'] = consequent
    features['Support'] = support
    features['Confidence'] = confidence
    features['Lift']= lift
    
    return(features)


# In[2]:


def compact_prune(noun_features, clean_review):
    temp = []
    #clean_review = text_clean(text)
    #noun = association(text)
    a = [''.join(x) for x in list(noun_features.Antecedent)]
    b = [''.join(x) for x in list(noun_features.Consequent)]
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
                if b[i] in words:
                    feature = (a[i],b[i])
                    first = words.index(a[i])
                    second = words.index(b[i])
                    if abs(first-second) < 4 :
                        if first < second:
                            if words[first+1:second] not in conj:
                                count=1
                        elif words[second+1:first] not in conj:
                            count=1
            counter.append(count)
        df[feature] = counter
        
    for i in df.columns:
        if df[i].sum() > 3:
            temp.append(i)
    df = df[temp]
    return(df)


# In[3]:


def text_bigrams(words):
    from nltk.collocations import BigramCollocationFinder
    from nltk.metrics import BigramAssocMeasures
    from nltk.corpus import stopwords
    nouns = []
    for i in words:
        for j in i:
            nouns.append(j)
    finder = BigramCollocationFinder.from_words(nouns)
    stop_words = stopwords.words('english')
    finder.apply_word_filter(lambda w: w in stop_words)
    bigrams = finder.nbest(BigramAssocMeasures.likelihood_ratio,100)
    bigram = pd.DataFrame({'Feature':bigrams})
    return(bigram)


# In[4]:


def extract_feature(feature_df,bigram):
    feature = pd.DataFrame(feature_df.columns,columns = ['Feature'])
    feature = pd.merge(feature,bigram,how='inner')
    bigram_list = list(bigram.Feature)
    feature = feature_df.iloc[:,feature_df.columns.isin(bigram_list)]
    return(feature)


# In[5]:


def extract_adjective1(df,clean_review):
    from nltk.tokenize import sent_tokenize
    import spacy
    nlp = spacy.load('en_core_web_sm')
#     clean_review = text_clean(review_text)
#     sent_list = tokenize(clean_review)     
#     for j in clean_review:
#         sent = sent_tokenize(j)
#         sent_list.append(sent)
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
                    first = words.index(i[0])
                    second = words.index(i[1])
                    if abs(first-second) < 4 :
                        if first < second:
                            if words[first+1:second] not in conj:
                                temp.append(sent)
                        elif words[second+1:first] not in conj:
                              #print(sent)
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
    def pos(text):
#         text = text_clean(text)
        pos_tags = []
        for i in text:
            doc = nlp(i)
            temp = []
            for token in doc:
                temp.append((token,token.pos_))
            pos_tags.append(temp)
        return(pos_tags)
    pos_tags = pos(reviews)
#     pos_tags = pos(reviews)
  
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
            
        adjective.append(temp)
    feature_review['Adjective'] = adjective
    
    nearest_adj = []
    for i in range(len(feature_review)):
        feature = feature_review.Feature[i].strip("()").replace("'",'').split(', ')
     
        sent = feature_review.Review[i]
        sent = sent.replace('.',' ')
      #print(tokens)
        try:
            feature_index1 = sent.index(feature[0])
            feature_index2 = sent.index(feature[1])
          #print(feature_index1,feature_index2)
            temp = []
            adj = []
            for adjective in feature_review.Adjective[i]:
                adj.append(adjective)
                temp.append(sent.index(adjective))
            diff = []
          #print(temp)
            for j in temp:
                diff.append(min(abs(feature_index1-j),abs(feature_index2-j)))
          #print(diff)
            idx = diff.index(min(diff))
            nearest_adj.append(adj[idx])
        except:
            nearest_adj.append('')
            continue
    feature_review['Nearest_Adjective'] = nearest_adj
    return(feature_review)


# In[6]:


def features(feature_list):
    import numpy as np
    _, idx = np.unique(feature_list, axis=1, return_index=True)
    feature_list = feature_list.iloc[:, idx]
    return(feature_list)


# In[7]:


def feature_value(cleaned,text,review, pos_tags):
    nouns=association(cleaned)
    df=compact_prune(nouns, text)
    bigram=text_bigrams(cleaned)
    feature=extract_feature(df,bigram)
    adjective_df = extract_adjective1(df,text)
    feature=features(feature)
    return(adjective_df,feature)


#! usr/bin/python
#coding=utf-8
# -*- coding:cp936 -*-

custom_stop = [
"\n",
"code"
]

import logging
#logging.basicConfig(level=logging.INFO,
#                    filename='new.log',
#                    filemode='w'
#                    )

import os
import json
from shutil import copyfile
from pathlib import Path
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction

output_path_Q = "../output/questionsMLHigh/"
output_path_A = "../output/answersMLHigh/"

from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")
    
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')
en_stop += custom_stop

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


import xml.etree.ElementTree

def custom_tokenizer(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if ((not i in en_stop) and (len(i) > 1 or i == "r") and (not i.isdigit()))]
    
    return stopped_tokens

all_texts = []
all_code_texts = []

for post_f in os.listdir(output_path_Q):
    if not post_f.endswith(".xml"):
        continue
    
    doc_pair = ""
    code_pair = ""
    
    qRoot = xml.etree.ElementTree.parse(output_path_Q+post_f).getroot()
    ## Parse XML
    post_id = qRoot.get('Id')
    answer_id = qRoot.get('AcceptedAnswerId')
    body = qRoot.get('Body')    
    tags = qRoot.get('Tags')
    title = qRoot.get('Title')
    

    ## clean html tags and code
    codeFinder = BeautifulSoup(body, 'lxml').findAll('code')
    code = "\n".join(str(tag).replace('&gt;','>').replace('&lt;','<') for tag in codeFinder)
    
    body = BeautifulSoup(body, "lxml")
    [_.extract() for _ in body('code')]
    body = body.text

    doc_pair += " "+body
    doc_pair += (" "+tags)*2
    doc_pair += (""+title)*2
    code_pair += " "+code
    
    answer_file = output_path_A+"post_"+answer_id+".xml"
    if Path(answer_file).exists():
        aRoot = xml.etree.ElementTree.parse(answer_file ).getroot()
        body = aRoot.get('Body')    
        
        codeFinder = BeautifulSoup(body, 'lxml').findAll('code')
        code = "\n".join(str(tag).replace('&gt;','>').replace('&lt;','<') for tag in codeFinder)
    
       
        body = BeautifulSoup(body, "lxml")
        [_.extract() for _ in body('code')]
        body = body.text
        doc_pair += " "+body
        code_pair += " "+code 

    texts = []
    code_texts = []
    
    ##
    raw = doc_pair.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if ((not i in en_stop) and (len(i) > 1 or i == "r") and (not i.isdigit()))]
    
    
    stemmed_stopped_tokens = [stemmer.stem(i) for i in tokens if ((not i in en_stop) and (len(i) > 1) and (not i.isdigit()))]
    
    # stem tokens
    #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    
    # add tokens to list
    #texts.append(stemmed_tokens)  
    texts += stopped_tokens
    texts_stemmed = stemmed_stopped_tokens
    

    ##
    code_raw = code_pair.lower()
    code_tokens = tokenizer.tokenize(code_raw)
    stopped_tokens = [i for i in code_tokens if ((not i in en_stop) and (len(i) > 1) and (not i.isdigit()))]
    
    stopped_tokens_stemmed = [stemmer.stem(i) for i in code_tokens if ((not i in en_stop) and (len(i) > 1) and (not i.isdigit()))]
    
    code_texts += stopped_tokens
        
    all_texts.append(doc_pair)
    all_code_texts.append(code_pair)

vocab_frame = pd.DataFrame({'words': texts}, index = texts_stemmed) 
   

from sklearn.feature_extraction.text import TfidfVectorizer

#define vectorizer parameters
tfidf_vectorizer = TfidfVectorizer(max_df=1.0, max_features=200000,
                                 min_df=0.1, stop_words=en_stop,
                                 use_idf=True, tokenizer=custom_tokenizer, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(all_texts)
code_tfidf_matrix = tfidf_vectorizer.fit_transform(all_code_texts)
terms = tfidf_vectorizer.get_feature_names()

from sklearn.cluster import KMeans    
num_clusters = 10
km = KMeans(n_clusters=num_clusters, init='random', max_iter=100, n_init=1, verbose=1)
text_km = km.fit(tfidf_matrix)
code_km = km.fit(code_tfidf_matrix)

text_clusters = text_km.labels_.tolist()
code_clusters = code_km.labels_.tolist()


post_dict = { 'text': all_texts, 'code': all_code_texts,  'cluster': text_clusters}
post_frame = pd.DataFrame(post_dict, index = [text_clusters] , columns = ['text', 'code', 'cluster'])

post_frame['cluster'].value_counts()


print("Top terms per cluster:")
print()
#sort cluster centers by proximity to centroid
order_centroids = text_km.cluster_centers_.argsort()[:, ::-1] 

for i in range(num_clusters):
    print("Cluster %d words:" % i, end='')
    
    for ind in order_centroids[i, :6]: #replace 6 with n words per cluster
        print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0], end=',')
    print() #add whitespace
    print() #add whitespace
    
## The result is not very helpful
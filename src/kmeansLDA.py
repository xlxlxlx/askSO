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

output_path_Q = "../output/questionsMLHigh/"
output_path_A = "../output/answersMLHigh/"

filter_rst = {}
    
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

out_f = "../output/ldaSumHigh.txt"

all_texts = []
all_code_texts = []

for post_f in os.listdir(output_path_Q):
    if not post_f.endswith(".xml"):
        continue
    
    doc_pair = []
    code_pair = []
    
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

    doc_pair.append(body)
    doc_pair.append(tags*2)
    doc_pair.append(title*2)
    code_pair.append(code)
    
    answer_file = output_path_A+"post_"+answer_id+".xml"
    if Path(answer_file).exists():
        aRoot = xml.etree.ElementTree.parse(answer_file ).getroot()
        body = aRoot.get('Body')    
        
        codeFinder = BeautifulSoup(body, 'lxml').findAll('code')
        code = "\n".join(str(tag).replace('&gt;','>').replace('&lt;','<') for tag in codeFinder)
    
       
        body = BeautifulSoup(body, "lxml")
        [_.extract() for _ in body('code')]
        body = body.text
        doc_pair.append(body)
        code_pair.append(code)
        
    #logging.info(doc_pair)     
    texts = []

    code_texts = []
    
    for doc in doc_pair:    
        # clean and tokenize document string
        raw = doc.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if ((not i in en_stop) and (len(i) > 1 or i == "r") and (not i.isdigit()))]
        
        # stem tokens
        #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        # add tokens to list
        #texts.append(stemmed_tokens)  
        texts += stopped_tokens     
    
    for code in code_pair:
        ## For code snippet
        code_raw = code.lower()
        code_tokens = tokenizer.tokenize(code_raw)
        stopped_tokens = [i for i in code_tokens if ((not i in en_stop) and (len(i) > 1) and (not i.isdigit()))]
        code_texts += stopped_tokens

    all_texts.append(texts)
    all_code_texts.append(code_texts)
    


#logging.info(texts)     
# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(all_texts)
code_dictionary = corpora.Dictionary(all_code_texts)
    
# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in all_texts]
code_corpus = [dictionary.doc2bow(text) for text in all_code_texts]


topic_k = 20
# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=topic_k, id2word = dictionary, passes=20)  
code_ldamodel = gensim.models.ldamodel.LdaModel(code_corpus, num_topics=topic_k, id2word = dictionary, passes=20) 

corpus_lda = ldamodel[corpus]
code_corpus_lda = ldamodel[code_corpus]

corpus_lda_dense = corpus2dense(corpus_lda, topic_k)
code_corpus_lda_dense = corpus2dense(code_corpus_lda, topic_k)


num_clusters = 10
km = KMeans(n_clusters=num_clusters, init='random', max_iter=100, n_init=1, verbose=1)
text_km = km.fit(corpus_lda_dense)
code_km = km.fit(code_corpus_lda_dense)



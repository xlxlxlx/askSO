custom_stop = [
"\n"
]

import logging
logging.basicConfig(level=logging.INFO,
                    filename='new.log',
                    filemode='w'
                    )

import os
import json
from shutil import copyfile
from pathlib import Path
from bs4 import BeautifulSoup

output_path_Q = "questionsML/"
output_path_A = "answersML/"

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


for post_f in os.listdir(output_path_Q):
    
    doc_pair = []
    
    qRoot = xml.etree.ElementTree.parse(output_path_Q+post_f).getroot()
    ## Parse XML
    post_id = qRoot.get('Id')
    answer_id = qRoot.get('AcceptedAnswerId')
    body = qRoot.get('Body')    
    tags = qRoot.get('Tags')

    ## clean html tags
    body = BeautifulSoup(body, "lxml").text

    doc_pair.append(body)
    doc_pair.append(tags)
    
    answer_file = output_path_A+"post_"+answer_id+".xml"
    if Path(answer_file).exists():
        aRoot = xml.etree.ElementTree.parse(answer_file ).getroot()
        body = aRoot.get('Body')    
        body = BeautifulSoup(body, "lxml").text
        doc_pair.append(body)
        
    #logging.info(doc_pair)     
    texts = []
    for doc in doc_pair:    
        # clean and tokenize document string
        raw = doc.lower()
        tokens = tokenizer.tokenize(raw)

        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        
        # stem tokens
        #stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        
        # add tokens to list
        #texts.append(stemmed_tokens)  
        texts.append(stopped_tokens)         
    
    #logging.info(texts)     
    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
        
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word = dictionary, passes=20)  

    print(ldamodel.print_topics(num_topics=2, num_words=4))  


    

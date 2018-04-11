## in both body and tags
keywords = [
"tensorflow",
" torch",
" theano", # TheAnonymousType
"caffe",
#"microsoft azure",
#"cuda", # it is related but too nvidia specific
"cntk",
"keras",

"machine learning",
"feature selection",
"tf-idf",
"neural network",
"deep learning",
"feature extraction",
"cluster analysis ",
"unsupervised learning",
"sentiment analysis",
"text mining",
" gmm",
"classification",
#"regression", # just regression
#"predict", #predicable
#"boost",
"bagging",

"bigdata",
#"analytics",

"speech recognition",
"acoustic model",
"image recognition",
"machine translation",
"gene network inference",

"knn",
"k-nn",
"nearest neighbor",
"random forest",
"logistic regression",
"linear regression",
"decision tree",
"bayesian network",
"naive bayes",
"multinomial naive",
" svm",
"limma",
" lars", #dollars
" lasso", #IsSubclassOf, classobj
"elastic net",
#"hmm", #Hmm
" dnn",
" rnn",
" cnn",
"neural network",
"topic analy",


"scikit",
"sklearn",
"cross_validation",
"feature_selection",
"ensemble method",
"naive_bayes",
"linear_model",
"neural_network",
"e1071",
"randomForest"

]

## Only in tags
keytags = [
## How to handle the tags
"<nlp>", #jnlp
"<lda>",
"topic-modeling"
"machine-learning",
"artificial-intelligence",
#"mathematical-optimization",
"grid-search",
#"data-science",
"neural-network",
"deep-learning",
"feature-extraction",
"cluster-analysis ",
"unsupervised-learning",
"sentiment-analysis",
"text-mining"
]


import os
import json
from shutil import copyfile
from pathlib import Path

output_question_path = "questionsCodeOrigin/"
output_answer_path = "answersCode/"

output_path_Q = "questionsML/"
output_path_A = "answersML/"

import xml.etree.ElementTree
from bs4 import BeautifulSoup


for post_f in os.listdir(output_question_path):
    qRoot = xml.etree.ElementTree.parse(output_question_path+post_f).getroot()
    post_id = qRoot.get('Id')
    answer_id = qRoot.get('AcceptedAnswerId')
    body = qRoot.get('Body')   
    ## handle it later
    code = BeautifulSoup(body, 'lxml').code
    ## ensure enough length of code snippet
    if len(str(code)) < 100:
        continue
    tags = qRoot.get('Tags')

    ## clean html tags
    body = BeautifulSoup(body, "lxml").text
    
    if any(keyword in body.lower() for keyword in keywords) or any(keytag in tags.lower() for keytag in keytags):        
        answer_file = output_answer_path+"post_"+answer_id+".xml"
        if Path(answer_file).exists():
            copyfile(output_question_path+"post_"+post_id+".xml", output_path_Q+"post_"+post_id+".xml")
            copyfile(answer_file, output_path_A+"post_"+answer_id+".xml")

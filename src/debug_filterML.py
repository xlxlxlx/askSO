## Can be read from a separate file to be consistent with the real filter
keywords = [
"tensorflow",
"torch",
"theano",
"caffe",
"azure",
"cntk",
"keras",


"machine learning",
"machine-learning",
"artificial-intelligence ",
"neural-network ",
"deep-learning",
"feature-extraction",
"feature selection",
"unsupervised-learning",
"tf-idf",
"cluster-analysis ",
"gmm",
"classification",
"regression",
"predict", #predicable
"boost",
"bagging",

"bigdata",
"analytics",
"data-science",

"nlp",
"sentiment-analysis",
"text-mining",
"speech recognition",
"acoustic model",
"image recognition",
"machine translation",
"gene network inference",


"mathematical-optimization",
"grid-search",

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
"svm",
"limma",
"lars", #dollars
"lasso",
"elastic net",
"hmm", #Hmm
"dnn",
"rnn",
"cnn",


"scikit",
"sklearn",
"cross_validation",
"feature_selection",
"ensemble",
"naive_bayes",
"linear_model",
"neural_network",
"e1071",
"randomForest"

]

import xml.etree.ElementTree
import sys


def detectKeyword(num):
    root = xml.etree.ElementTree.parse("post_"+str(num)+".xml").getroot()
    for keyword in keywords:
        if keyword in root.get('Body').lower() or keyword in root.get('Tags').lower():
            print(keyword)

## Usage: ./detectKeyword.py <postID>
if __name__ == '__main__':
    id = sys.argv[1]
    detectKeyword(id)
    
    
    
import random
import numpy as np
import pandas as pd	
from pandas import Series
from scipy.sparse import csr_matrix
import scipy
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import cross_val_score



tablepath = "../output/"
df = pd.read_table(tablepath+"ldaSumHigh_code.csv", delimiter=",",  names = ['post','keyword'])

## Feature selection: 2 < frequency 
df = df.groupby("keyword").filter(lambda x: len(x) > 2)

## Save the predictors for predicting stage
df.keyword.drop_duplicates().to_csv(tablepath+'ldaSumHigh_code_predictors.csv', index = False)

## Generate a sparse matrix on selected like_ids and users
df['bool'] = Series(np.asarray([1]*len(df)), index=df.index)
post_u = list((df.post.unique()))
kw_u = list((df.keyword.unique()))
data = df['bool'].tolist()
row = df.post.astype('category', categories=user_u).cat.codes
col = df.keyword.astype('category', categories=like_u).cat.codes
sparse_matrix = csr_matrix((data, (row, col)), shape=(len(user_u), len(like_u)))

## Use the sparse matrix as training data
df_sparse_matrix = pd.DataFrame(sparse_matrix.todense(), index = post_u, columns = kw_u)


##### Method 2: Apply SVD 
## Apply SVD, k = 300
sparse_matrix =  sparse_matrix.asfptype()
U, s, V = scipy.sparse.linalg.svds(sparse_matrix, k = 20)
S = scipy.linalg.diagsvd(s, len(V), len(V))
print(U.shape)
print(S.shape)
print(V.shape)
df_SVD = pd.DataFrame(np.dot(U,S),index = user_u)

## Method 1
df = df_sparse_matrix 
df = df.rename(columns = {'fit': 'fit_feature'})
## Method 2
df = df_SVD




##### Training Stage for both methods #####

## Define the path of training profile data
df_meta = pd.read_table(tablepath+"postHighmeta.csv", delimiter=",",index_col = 0)
features = list(df_meta.columns)
df_meta = df_meta[features]
df_train = df.join(df_meta)

## Only python
df_train = df_train.loc['python' in df_train['lan']]

df_train_related = df_train.loc[df_train['related'] == 1]
df_train_type = df_train_related.groupby("type").filter(lambda x: len(x) > 5)

## Define the features
feature_cols = df_train.columns.values[0:-6]


## Train the models and perform 10-fold CV
def training(label_col, df_train):
    X = df_train[feature_cols]
	y = df_train.loc[:,label_col]
	
	
	clf = svm.SVC()
	#clf = LogisticRegression()
		
	scores = cross_val_score(clf, X, y, cv=10,scoring='accuracy')
	print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
	clf.fit(X, y)
	joblib.dump(clf, 'svm_%s.pkl' %label_col) 

def training_multi(label_col, df_train):
    X = df_train[feature_cols]
	y = df_train.loc[:,label_col]
	
	clf = svm.LinearSVC()
	#clf = LogisticRegression()
		
	scores = cross_val_score(clf, X, y, cv=5,scoring='accuracy')
	print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
	clf.fit(X, y)
	joblib.dump(clf, 'svm_%s.pkl' %label_col) 


for label in ['related']:
	print(label)
	training(label, df_train)

for label in ['sta']:
	print(label)
	training(label, df_train_related)

for label in ['type']:
	print(label)
	training_multi(label, df_train_type)


	


		


import numpy as np
import pandas as pd
import scipy
from scipy.sparse import csr_matrix
from sklearn.externals import joblib


tablepath = "../output/"
df = pd.read_table(tablepath+"ldaSumMed_code.csv", delimiter=",",  names = ['post','keyword'])

## Define location of predictors
## eg. predictors/
predictor_path = "../output/"

## Define location of models
## eg. models/
model_path = "code/"

## Read the predefined predictors
df_predictor = pd.read_csv(predictor_path+"ldaSumHigh_code_predictors.csv", delimiter=",", header=0)
predictor_list = df_predictor['keyword'].tolist()

## Filter test data
df = df[df['keyword'].isin(predictor_list)]


## Generate a sparse matrix
df['bool'] = np.asarray([1]*len(df))
post_u= list((df.post.unique()))
kw_u = list((df.keyword.unique()))
data = df['bool'].tolist()
row = df.post.astype('category', categories=post_u).cat.codes
col = df.keyword.astype('category', categories=kw_u).cat.codes

sparse_matrix = csr_matrix((data, (row, col)), shape=(len(post_u), len(kw_u)))

##### Method 1: sparse matrix#####
sparse_matrix_df = pd.DataFrame(sparse_matrix.todense(), index = post_u, columns = kw_u)

## If a selected keyword is not in the test data, add a column of "0"s for it. 
if len(sparse_matrix_df.columns) < len(predictor_list):
     for item in list(set(predictor_list) - set(list(sparse_matrix_df.columns))):
      #print(item)
      sparse_matrix_df[item] = np.zeros(len(sparse_matrix_df))
 
df_test = sparse_matrix_df
X = df_test





##### Prediction for either of the method #####
df_return = pd.DataFrame(list((df_test.index)),columns = ['post'])

method = "dense"
def svm_lrg_predict(label_col):		
    
    ## Load pre-trained models
    if label_col not in ['related','sta','type']:
        return

    clf = joblib.load(model_path+'lgr_%s_%s.pkl' %(label_col, method)) 


    y_pred = clf.predict(X)
    df_return[label_col] = y_pred


for label in ['related','sta','type']:
    svm_lrg_predict(label)


df_return.to_csv('predict_ldaSumMed_code.csv', index = False)





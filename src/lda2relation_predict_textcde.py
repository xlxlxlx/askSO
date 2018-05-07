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
model_path = "textcode/"

## Read the predefined predictors
df_predictor = pd.read_csv(predictor_path+"ldaSumHigh_textcode_predictors.csv", delimiter=",", header=0)
predictor_list = df_predictor['keyword'].tolist()




def sparseMatrixify(fn, method):
    df = pd.read_table(tablepath+fn+".csv", delimiter=",",  names = ['post','keyword'])


    #df = df.rename(columns = {'fit': 'fit_feature'})
    #df = df.rename(columns = {'type': 'type_feature'})

    if "code" in fn:
        df['keyword'] = 'code_' + df['keyword'].astype(str)

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


    if method == "dense":
        sparse_matrix_df = pd.DataFrame(sparse_matrix.todense(), index = post_u, columns = kw_u)
        df = sparse_matrix_df

    elif method == "SVD":
    ## Method 2
        sparse_matrix =  sparse_matrix.asfptype()
        U, s, V = scipy.sparse.linalg.svds(sparse_matrix, k = 20)
        S = scipy.linalg.diagsvd(s, len(V), len(V))
        df_SVD = pd.DataFrame(np.dot(U,S),index = post_u)
        df = df_SVD

    return df

method = "dense"
mdl = "lgr"

df_code = sparseMatrixify('ldaSumMed_code', method)
df_text = sparseMatrixify('ldaSumMed_text', method)

df = df_code.join(df_text, how = 'inner')
sparse_matrix_df = df

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


df_return.to_csv('predict_ldaSumMed_textcode.csv', index = False)





import os 
import h5py 
import sklearn 
import datetime 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from os.path import join 
from functools import partial 
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn import metrics

from imputation import *

# We input the preprocessed data. 
rawdata=pd.read_csv('scaled_counts.csv',sep='\t',header=None,index_col=None)
data_norm = rawdata.values
data_norm1 = data_norm.copy()

# We set the number of cluster by calculating the silhouette coefficient. 
label_path = "label.csv"
label = np.loadtxt(label_path, delimiter='\t')

#pca
num_components=30 #The number of principal components at least explains 40% of the variance in the data
pca = PCA(n_components=num_components,svd_solver = "randomized")
pca_data = pca.fit_transform(data_norm)
print(pca_data.shape)


#K-means
clusters=len(np.unique(label))
print('clusters:',clusters)
kmeans = KMeans(n_clusters=clusters, random_state=0).fit(pca_data)
label_pr =  kmeans.labels_
print('label_pr:',label_pr)
print('length:',len(label_pr))
np.savetxt('label2.csv', label_pr, fmt='%0.5f', delimiter='\t', header='label')

#The identification of dropout events
st = datetime.datetime.now()

def identify_dropout(cluster_cell_idxs, X):
    for idx in cluster_cell_idxs:
        dropout=(X[:,idx]==0).sum(axis=1)/(X[:,idx].shape[1])
        dropout_thr=0.5
        dropout_upper_thr,dropout_lower_thr = np.nanquantile(dropout,q=dropout_thr),np.nanquantile(dropout,q=0)
        gene_index1 = (dropout<=dropout_upper_thr)&(dropout>=dropout_lower_thr)
        #print(gene_index1)
        cv = X[:,idx].std(axis=1)/X[:, idx].mean(axis=1)
        cv_thr=0.5
        cv_upper_thr,cv_lower_thr = np.nanquantile(cv,q=cv_thr),np.nanquantile(cv,q=0)
        #print(cv_upper_thr,cv_lower_thr)
        gene_index2 = (cv<=cv_upper_thr)&(cv>=cv_lower_thr)
        #print(gene_index2)
        #include_faslezero_gene= list(np.intersect1d(gene_index1,gene_index2))
        include_faslezero_gene = np.logical_and(gene_index1, gene_index2)
        #print(list(include_faslezero_gene).count(True))
        tmp = X[:, idx]
        tmp[include_faslezero_gene] = tmp[include_faslezero_gene]+(tmp[include_faslezero_gene]==0)*-1
        X[:, idx] = tmp
    return X

label_set = np.unique(label_pr)
cluster_cell_idxs = list(map(partial(find_cluster_cell_idx,label=label_pr), label_set))
data_identi=identify_dropout(cluster_cell_idxs, X=data_norm.T)

ed = datetime.datetime.now()   
print('identify_dropout ：', (ed - st).total_seconds())

#The imputation of dropout events
st = datetime.datetime.now()
cluster_samples=list(map(partial(find_cluster_samples,X=data_identi),cluster_cell_idxs))
cluster_cell_stats = list(map(partial(find_cluster_gene_mean, X=data_identi),cluster_cell_idxs))
other_cluster_cell_idxs = list(map(partial(find_othercluster_cell_idx, label=label_pr), label_set))
other_cluster_cell_stats = list(map(partial(find_othercluster_gene_mean_std, X=data_identi),other_cluster_cell_idxs))

global_std = list(map(lambda x:(x[x>=0]).std(),data_identi))

X_imputed = map(partial(imputation_for_cell, 
                X=data_identi, 
                labels=label_pr, 
                global_std=global_std,
                cluster_samples=cluster_samples,
                same_cluster_stats=cluster_cell_stats,
                other_cluster_stats=other_cluster_cell_stats),
                np.arange(data_identi.shape[1])
               )

X_imputed = np.array(list(X_imputed)).T
data_imputed = data_norm1 + (data_identi==-1).T * X_imputed.T

df_imputed = pd.DataFrame(data_imputed)
df_imputed.to_csv('imputed_counts.csv', sep='\t')

ed = datetime.datetime.now()
(ed - st).total_seconds()
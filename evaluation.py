import time
import pandas as pd
import numpy as np
import sklearn
from sknetwork.clustering import Louvain
from sklearn.metrics.cluster import normalized_mutual_info_score
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.cluster import KMeans


input_path = "scaled_counts.csv"
# input = pd.read_csv(input_path,sep='\t',index_col=0)
# input = input.T
input = pd.read_csv(input_path,sep='\t',header=None,index_col=None)
input = input

label_path = "label2.csv"
y_true = np.loadtxt(label_path, delimiter='\t',skiprows=1)


imputedData=pd.read_csv('imputed_counts.csv',sep='\t',header=0,index_col=0)
imputedData=imputedData
print(input.shape,imputedData.shape,y_true.shape,imputedData.head())


start = time.time()

def validate_origin(original_data,true_label):
    print('start evaluating original_data....')
    lab_num=len(np.unique(true_label))
    print(lab_num)
    pearson_sim = np.corrcoef(original_data)
    ##--------------louvain clustering-----------
    #louvain = Louvain()
    #lv_pre = louvain.fit_transform(pearson_sim)
    #nmi_louvain = format(normalized_mutual_info_score(true_label, lv_pre), '.5f')
    #ari_louvain = format(adjusted_rand_score(true_label, lv_pre), '.5f')
    #print('nmi and ari of original data with louvain clustering: ',
    #      str(nmi_louvain), str(ari_louvain))
    ##------------kmeans clustering------------
    estimators = KMeans(n_clusters=lab_num)
    est = estimators.fit(original_data)
    kmeans_pred = est.labels_
    nmi_kmeans = format(normalized_mutual_info_score(true_label, kmeans_pred), '.5f')
    ari_kmeans = format(adjusted_rand_score(true_label, kmeans_pred), '.5f')
    print('nmi and ari of original data with kmeans clustering: ',
          str(nmi_kmeans), str(ari_kmeans))
    ##-------------pearson spectral clustering---------------
    sc_pred = sklearn.cluster.SpectralClustering(n_clusters=lab_num, affinity='precomputed').fit_predict(pearson_sim)
    nmi_spectral = format(normalized_mutual_info_score(true_label, sc_pred), '.5f')
    ari_spectral = format(adjusted_rand_score(true_label, sc_pred), '.5f')

    print('nmi and ari of original data with pearson spectral clustering: ',
          str(nmi_spectral), str(ari_spectral))

    return nmi_kmeans, nmi_spectral, ari_kmeans, ari_spectral

end = time.time()
print ('time:',end-start)


start = time.time()
def validate_imputation(imputed_data, true_label):
    print('start evaluating imputation....')
    lab_num = len(np.unique(true_label))
    pearson_sim = np.corrcoef(imputed_data) 
    ##--------------louvain clustering-----------
    #louvain = Louvain()
    #lv_pre = louvain.fit_transform(pearson_sim)
    #nmi_louvain = format(normalized_mutual_info_score(true_label, lv_pre), '.5f')
    #ari_louvain = format(adjusted_rand_score(true_label, lv_pre), '.5f')
    #print('nmi and ari of imputed data with louvain clustering: ',
    #      str(nmi_louvain), str(ari_louvain))
    ##------------kmeans clustering------------
    estimators = KMeans(n_clusters=lab_num)
    est = estimators.fit(imputed_data)
    kmeans_pred = est.labels_
    nmi_kmeans = format(normalized_mutual_info_score(true_label, kmeans_pred), '.5f')
    ari_kmeans = format(adjusted_rand_score(true_label, kmeans_pred), '.5f')
    print('nmi and ari of imputed data with kmeans clustering: ',
          str(nmi_kmeans), str(ari_kmeans))
    ##-------------pearson spectral clustering---------------
    sc_pred = sklearn.cluster.SpectralClustering(n_clusters=lab_num, affinity='precomputed').fit_predict(pearson_sim)
    nmi_spectral = format(normalized_mutual_info_score(true_label, sc_pred), '.5f')
    ari_spectral = format(adjusted_rand_score(true_label, sc_pred), '.5f')

    print('nmi and ari of imputed data with pearson spectral clustering: ',
          str(nmi_spectral), str(ari_spectral))
    
    
    return nmi_kmeans, nmi_spectral, ari_kmeans, ari_spectral

end = time.time()
print ('time:',end-start)  



start = time.time()

[nmi_kmeans1, nmi_spectral1, ari_kmeans1, ari_spectral1] = validate_origin(input,y_true)
print(nmi_kmeans1, nmi_spectral1, ari_kmeans1, ari_spectral1)

[nmi_kmeans2, nmi_spectral2, ari_kmeans2, ari_spectral2] = validate_imputation(imputedData, y_true)
print(nmi_kmeans2, nmi_spectral2, ari_kmeans2, ari_spectral2)


# result=[[nmi_louvain1, nmi_kmeans1, nmi_spectral1, ari_louvain1, ari_kmeans1, ari_spectral1],
#        [nmi_louvain2, nmi_kmeans2, nmi_spectral2, ari_louvain2, ari_kmeans2, ari_spectral2]]

end = time.time() 
print ('time:',end-start)



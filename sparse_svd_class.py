# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:19:21 2016

@author: bstange
"""
import scipy as sc
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

class sparse_svd(object):
    """
    
    """   
    def __init__(self, i, j, v, components = 10, tfidf=False, random_state = 42):
        """ 
        Takes sparse triple and transforms to a specified number of components.
        
        Parameters
        ----------
        i, j, v : row, column, and value
        
        components : specified number of columns to return
        
        tfidf : True will tfidf transform the sparse matrix before reducing dimensionality
        
        Returns 
        ----------
        Object which contains the input lists, svd object and output matrix.

        """
        self.row_u = list(sorted(i.unique()))
        self.col_u = list(sorted(j.unique()))
        self.values = v.tolist()
        self.csr = sc.sparse.csr_matrix((self.values, (i.astype('category',categories=self.row_u).cat.codes, 
                                                       j.astype('category',categories=self.col_u).cat.codes)),
                                        shape=(len(self.row_u),len(self.col_u)))
        if tfidf:
            self.tf_trans = TfidfTransformer()
            self.csr = self.tf_trans.fit_transform(self.csr)
        self.svd = TruncatedSVD(n_components=components, random_state=random_state).fit(self.csr)
        #self.svd_mat = self.svd.fit_transform(self.csr)
        self.svd_mat = pd.DataFrame(self.svd.fit_transform(self.csr), index = self.row_u)

    def GetImportantComponents(self, index, cutoff):
        """
        Takes column index (0 to m-1) and returns all original columns with |weights| >= cutoff
        """
        s = pd.Series(self.svd.components_[index,:], index=self.col_u)
        s = s[abs(s) >= cutoff]
        s = s.sort_values(ascending = False)
        return s

    def GetColumnAggregate(self, col_name):
        """
        Takes column name and returns frequency (percent) and avg number of items per instance.
		Doesn't work with tfidf transform.  Needs fix.
        """
        total = len(self.csr.getcol(self.col_u.index(col_name)).nonzero()[0]) / self.csr.shape[0]
        avg = self.csr.getcol(self.col_u.index(col_name))[self.csr.getcol(self.col_u.index(col_name)).nonzero()[0]].mean()
        return {"Percent with >=1": total, "Avg per record": avg}
    
    def WriteToCSV(self, file):
        #np.savetxt(file,self.svd_mat, delimiter=",")
        self.svd_mat.to_csv(file, header = False)

if __name__=="__main__":
	
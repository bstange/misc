# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 15:21:00 2018

@author: xvnq1898
"""


import textract
import os
import json

import numpy as np
import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import matplotlib as mpl

def get_ppts(directory):
    """
    args: directory
    output: dict of files, content
    """
    flist = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.pptx'):
                try:
                    text = textract.process(os.path.join(root, file)).decode('utf-8')
                    flist[os.path.join(root, file)] = text.replace('\r\n', ' ').replace('\n',' ').replace('\r', ' ')
                    print(os.path.join(root, file))
                except Exception as e:
                    print(e)
    return flist

def get_ppt_distances(ppts):
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")
    
    labels = []
    text = []
    for i, value in ppts.items():
        labels.append(i)
        text.append(value)
    
    #CountVectorizer().build_tokenizer()(text)
    
    short_labels = [os.path.basename(i) for i in labels]
    
    def tokenize_and_stem(text):
        # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
        tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
        filtered_tokens = []
        # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
        for token in tokens:
            if re.search('[a-zA-Z]', token):
                filtered_tokens.append(token)
        stems = [stemmer.stem(t) for t in filtered_tokens]
        return stems
    
    tfidf_vectorizer = TfidfVectorizer(max_df=.8, max_features=200000, min_df=.05,
                                       stop_words='english',use_idf=True,
                                       tokenizer=tokenize_and_stem, ngram_range=(1,3))
    
    tfidf_matrix = tfidf_vectorizer.fit_transform(text)
#    terms = tfidf_vectorizer.get_feature_names()
    
    dist = 1 - cosine_similarity(tfidf_matrix)
    return dist, short_labels

def dendrogram_from_DistMat(dist, labels, image_file):
    linkage_matrix = ward(dist)

    fig, ax = plt.subplots(figsize=(15, 15)) # set size, needs to adjusted
    ax = dendrogram(linkage_matrix, orientation="right", labels=labels);
    
    plt.tick_params(\
        axis= 'x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')
    
    plt.tight_layout() #show plot with tight layout
    
    plt.savefig(image_file, dpi=200) #save figure

if __name__ == '__main__':
    outtext = 'ppt_text.txt' # will write to current directory, or specify full path
    directory = '.\\ppts'# directory to recursively scan for powerpoint files
    outdend = 'dend.png'
    
    ppts = get_ppts(directory)
    with open(outtext, 'w') as out:
        json.dump(ppts, out, indent=4)
    dist, short_labels = get_ppt_distances(ppts)
    dendrogram_from_DistMat(dist,short_labels,outdend)
    
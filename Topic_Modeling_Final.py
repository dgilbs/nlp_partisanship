import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import random
import seaborn as sns
import pickle

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.metrics import pairwise_distances
from sklearn.manifold import TSNE
from sklearn.externals import joblib
from sklearn.cluster import KMeans, DBSCAN, AffinityPropagation
from nltk.corpus import stopwords
from collections import defaultdict, Counter


def fit_tfidf(df):

    my_stops = stopwords.words()
    leg_df = pd.read_csv("data/legislators-current.csv")
    last_names = [name.lower() for name in list(leg_df.last_name)]
    my_stops += last_names
    excess_words = ["statement", "congress", "senator", "senate", "congressman", "committee", "whether", "role","since",
                   "united", "states", "well", "much", "department", "congress", "like", "senators", "two", "three",
                   "mr", "ms", "chairman", "ranking", "member", "republicans", "democrats", "republican", "democratic",
                   "democrat", "put", "going", "said", "needs" ,"see", "get", "back", "going", "way", "last", "could"]
    my_stops += excess_words
    all_releases = list(df["Release"])
    corpus = list()
    lengths = defaultdict(int)
    for index, release in enumerate(all_releases):
        sents = nltk.sent_tokenize(release)
        lengths[index] = len(sents)
        corpus += sents

    tfidf = TfidfVectorizer(max_df=0.95, min_df=0.01, stop_words=my_stops,
                            token_pattern="\\b[a-z][a-z]+\\b", ngram_range=(1, 2))

    rel_tf = tfidf.fit_transform(corpus)

    return rel_tf





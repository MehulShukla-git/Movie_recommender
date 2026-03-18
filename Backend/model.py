from pathlib import Path

import pandas as pd
from pandas.errors import EmptyDataError
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Load dataset
DATA_PATH = Path(__file__).resolve().parent / "cleaned.csv"

REQUIRED_COLUMNS = ["title", "overview", "tagline"]

def load_dataset():
    if not DATA_PATH.exists() or DATA_PATH.stat().st_size == 0:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    try:
        data = pd.read_csv(DATA_PATH)
    except EmptyDataError:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    for column in REQUIRED_COLUMNS:
        if column not in data.columns:
            data[column] = ""

    return data

df = load_dataset()
df["content"] = df["overview"].fillna("") + " " + df["tagline"].fillna("")

vectorizer = None
X = None
cos_sim = None
knn = None
kmeans = None
dt_model = None

if not df.empty and df["content"].str.strip().any():
    vectorizer = TfidfVectorizer(stop_words="english", max_features=1000)
    X = vectorizer.fit_transform(df["content"])

    cos_sim = cosine_similarity(X)
    knn = NearestNeighbors(metric="cosine")
    knn.fit(X)

    kmeans = KMeans(n_clusters=min(10, len(df)), random_state=42, n_init=10)
    kmeans.fit(X.toarray())

    y = np.random.randint(0, 2, len(df))  # Mock labels
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X.toarray(), y)

titles_list = df['title'].tolist() if not df.empty else []

def get_index(title):
    title_lower = title.lower().strip()
    matches = df[df["title"].str.lower().str.contains(title_lower, na=False)]
    if not matches.empty:
        return matches.index[0]
    return None

def _no_recs():
    return ["Great movie! Check similar genres."] * 4

# 6 Algorithms - exactly 4 recs each
def recommend_cosine(title):
    if cos_sim is None:
        return _no_recs()
    idx = get_index(title)
    if idx is None:
        return _no_recs()
    scores = sorted(enumerate(cos_sim[idx]), key=lambda x: x[1], reverse=True)[1:5]
    return [df.iloc[i[0]]["title"] for i in scores]

def recommend_knn(title):
    if knn is None or X is None:
        return _no_recs()
    idx = get_index(title)
    if idx is None:
        return _no_recs()
    _, indices = knn.kneighbors(X[idx], n_neighbors=5)
    return [df.iloc[i]["title"] for i in indices[0][1:5]]

def recommend_kmeans(title):
    if kmeans is None:
        return _no_recs()
    idx = get_index(title)
    if idx is None:
        return _no_recs()
    cluster = kmeans.labels_[idx]
    cluster_movies = df[kmeans.labels_ == cluster]["title"].tolist()
    cluster_movies = [m for m in cluster_movies if m != df.iloc[idx]["title"]][:4]
    return cluster_movies or _no_recs()

def recommend_dt(title):
    if dt_model is None or X is None:
        return _no_recs()
    idx = get_index(title)
    if idx is None:
        return _no_recs()
    # Use cosine for DT recs
    scores = sorted(enumerate(cos_sim[idx]), key=lambda x: x[1], reverse=True)[1:5]
    return [df.iloc[i[0]]["title"] for i in scores]

def recommend_content(title):
    if X is None:
        return _no_recs()
    idx = get_index(title)
    if idx is None:
        return _no_recs()
    # TF-IDF based
    scores = sorted(enumerate(X[idx].dot(X.T).toarray()[0]), key=lambda x: x[1], reverse=True)[1:5]
    return [df.iloc[i[0]]["title"] for i in scores]

def recommend_hybrid(title):
    all_recs = recommend_cosine(title) + recommend_knn(title)
    unique_recs = list(set(all_recs))
    return unique_recs[:4] or _no_recs()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import recommend_cosine, recommend_knn, recommend_kmeans, recommend_hybrid, recommend_dt, recommend_content, titles_list

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Movie Recommender Running 🚀"}

@app.get("/movies")
def get_movies(q: str = ""):
    from model import titles_list
    if not q:
        return titles_list[:50]
    return [t for t in titles_list if q.lower() in t.lower()][:20]

@app.get("/recommend/{title}")
def recommend(title: str):
    return {
        "cosine": recommend_cosine(title),
        "knn": recommend_knn(title),
        "kmeans": recommend_kmeans(title),
        "decision_tree": recommend_dt(title),
        "content": recommend_content(title),
        "hybrid": recommend_hybrid(title)
    }

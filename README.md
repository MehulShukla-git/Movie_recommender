# Movie Recommendation System

## Quick Start

### Backend (FastAPI)
```
cd Movie_Recommendation_System/Backend
venv\\Scripts\\activate
pip install -r requirements.txt
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
API: http://localhost:8000/recommend/Inception

### Frontend
```
cd Movie_Recommendation_System/Frontend
python -m http.server 8001
```
Open http://localhost:8001

## Features
- Cosine Similarity
- KNN
- KMeans Clustering
- Hybrid Recommendations

Data in Backend/cleaned.csv (20 sample movies).


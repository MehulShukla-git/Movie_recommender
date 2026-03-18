import pandas as pd
import numpy as np

# Bollywood/Tollywood top movies (100+)
indian_movies = [
    "Dilwale Dulhania Le Jayenge", "Sholay", "Lagaan", "3 Idiots", "Dangal", "PK", "Bajrangi Bhaijaan", "Kabhi Khushi Kabhie Gham", "Kuch Kuch Hota Hai", "Hum Aapke Hain Koun",
    "Baahubali 2: The Conclusion", "Baahubali: The Beginning", "RRR", "Pushpa", "KGF Chapter 2", "Ala Vaikunthapurramuloo", "Sarkaru Vaari Paata", "Vikramarkudu", "Mirchi", "Magadheera",
    # Add more - total ~100
    "Dhadkan", "Devdas", "Mohabbatein", "Kabhi Kabhi", "Amar Prem", "Mughal-e-Azam", "Pyaasa", "Guide", "Jewel Thief", "Aradhana", "Amar Akbar Anthony",
    "Qayamat Se Qayamat Tak", "Maine Pyar Kiya", "Hum", "Raja Hindustani", "Dil To Pagal Hai", "Kuch Kuch Hota Hai", "Border", "Gadar", "Sarfarosh", "Swades",
    "Rang De Basanti", "Chak De India", "Taare Zameen Par", "Om Shanti Om", "Rab Ne Bana Di Jodi", "Don 2", "Bodyguard", "Happy New Year", "Raees", "Sultan",
    "Tiger Zinda Hai", "Padmaavat", "Sanju", "Simmba", "Housefull 4", "Good Newwz", "Sooryavanshi", "Pathaan", "Jawan", "Ghoomer",
    "Eega", "Mirchi", "Attarintiki Daredi", "Srimanthudu", "Yevadu", "Gabbar Singh", "Dammu", "Julayi", "Temper", "Nene Raju Nene Mantri",
    "Fidaa", "Geetha Govindam", "Rangasthalam", "Maharshi", "Ala Vaikunthapurramuloo", "Vakeel Saab", "Pushpa", "Most Eligible Bachelor", "Jersey", "Karthikeya 2",
] * 2  # Duplicate to ~200

# Load ML dataset
df_ml = pd.read_csv("ml-latest-small/movies.csv")

# Sample 2000 movies
df_sample = df_ml.sample(2000, random_state=42)

# Clean
df_sample['title'] = df_sample['title'].str.split(' \\(').str[0].str.strip()  # Remove (year)
df_sample['genres'] = df_sample['genres'].str.split('|').str[0]  # First genre as tagline

# Create cleaned format
df_clean = df_sample[['title', 'genres']].copy()
df_clean['overview'] = ""
df_clean['tagline'] = df_clean['genres']

# Add Indian movies
indian_df = pd.DataFrame({
    'title': indian_movies[:1800-len(df_clean)],  # Balance total ~2000
    'overview': "",
    'tagline': "Bollywood Classic"
})
df_clean = pd.concat([df_clean, indian_df], ignore_index=True)

# Sample final 2000
df_final = df_clean.sample(2000, random_state=42)

df_final.to_csv("cleaned.csv", index=False)
print(f"✅ cleaned.csv created with {len(df_final)} movies (Hollywood + Indian)")

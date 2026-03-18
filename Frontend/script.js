const API = "http://127.0.0.1:8000";

const movieInput = document.getElementById("movie");
const loading = document.getElementById("loading");
const results = document.getElementById("results");

// Main recommendation function
async function getMovies() {
  const movie = movieInput.value.trim();
  
  if (!movie) {
    alert("Please enter a movie title");
    return;
  }

  loading.classList.remove("hidden");
  results.innerHTML = "";

  try {
    const res = await fetch(`${API}/recommend/${encodeURIComponent(movie)}`);
    
    if (!res.ok) {
      throw new Error("API unavailable - backend not running on port 8000");
    }
    
    const data = await res.json();

    loading.classList.add("hidden");

    // Display all 6 algorithm sections
    displaySection("⭐ HYBRID (Best)", data.hybrid || []);
    displaySection("🎯 COSINE SIMILARITY", data.cosine || []);
    displaySection("🔍 KNN", data.knn || []);
    displaySection("📊 K-MEANS", data.kmeans || []);
    displaySection("🌳 DECISION TREE", data.decision_tree || []);
    displaySection("⚡ CONTENT BASED", data.content_based || []);

  } catch (error) {
    loading.classList.add("hidden");
    results.innerHTML = `
      <div class="algo-section error">
        <h2>❌ Connection Error</h2>
        <div class="movie-card error">
          Backend not responding on localhost:8000<br>
          <small>${error.message}</small>
        </div>
      </div>
    `;
  }
}

function displaySection(title, movies) {
  if (!movies || movies.length === 0) {
    movies = ["No recommendations found"];
  }

  const section = document.createElement("div");
  section.className = "algo-section";

  section.innerHTML = `
    <h2>${title}</h2>
    <div class="card-grid">
      ${movies.slice(0, 4).map(movie => `<div class="movie-card">${movie}</div>`).join("")}
    </div>
  `;

  results.appendChild(section);
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  // Enter key
  movieInput.addEventListener("keypress", function(e) {
    if (e.key === "Enter") {
      getMovies();
    }
  });

  // Random button
  const randomBtn = document.getElementById('randomBtn');
  if (randomBtn) {
    randomBtn.onclick = async () => {
      try {
        const response = await fetch(`${API}/movies`);
        const movies = await response.json();
        const randomMovie = movies[Math.floor(Math.random() * movies.length)];
        movieInput.value = randomMovie;
        getMovies();
      } catch (e) {
        alert('Backend offline');
      }
    };
  }

  // Auto-focus
  movieInput.focus();
  
  // Autocomplete
  movieInput.addEventListener('input', async function() {
    const query = this.value.trim();
    if (query.length < 2) return;
    
    try {
      const response = await fetch(`${API}/movies?q=${encodeURIComponent(query)}`);
      const movies = await response.json();
      const datalist = document.getElementById('movie-list');
      datalist.innerHTML = movies.slice(0,10).map(m => `<option value="${m}">`).join('');
    } catch (e) {
      // Silent fail
    }
  });
});

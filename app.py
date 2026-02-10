"""
CineMatch AI — Full Stack Web App
Flask Backend + Gemini AI + TMDB API
Production-ready with comprehensive error handling
"""

from flask import Flask, render_template, request, jsonify, session
import requests
import google.generativeai as genai
import os
import json
import re
import logging
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cinematch-secret-2024-fallback")

# ── API Keys (must be set as environment variables) ──────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
TMDB_API_KEY   = os.environ.get("TMDB_API_KEY")

# Validate required environment variables
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable is not set!")
if not TMDB_API_KEY:
    logger.error("TMDB_API_KEY environment variable is not set!")

TMDB_BASE      = "https://api.themoviedb.org/3"
TMDB_IMG       = "https://image.tmdb.org/t/p/w500"
TMDB_IMG_SMALL = "https://image.tmdb.org/t/p/w185"

# ── Init Gemini with error handling ──────────────────────────────────
gemini_model = None
try:
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="""You are CineMatch AI, a cinematic and enthusiastic movie recommendation expert.
You have deep knowledge of world cinema — Hollywood, Bollywood, Tollywood, Korean, and beyond.
When recommending movies, be specific, insightful, and passionate.
Always respond in valid JSON when asked for structured data.
For chat responses, be conversational, warm, and knowledgeable."""
        )
        logger.info("Gemini AI initialized successfully")
    else:
        logger.warning("Gemini API key not found - AI features will be disabled")
except Exception as e:
    logger.error(f"Failed to initialize Gemini: {e}")
    gemini_model = None

# ── Error Handler Decorator ──────────────────────────────────────────
def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {str(e)}", exc_info=True)
            return jsonify({
                "error": "An error occurred processing your request",
                "message": str(e)
            }), 500
    return decorated_function

# ── TMDB Helper with improved error handling ─────────────────────────
def tmdb_get(endpoint, **params):
    """Make TMDB API request with error handling"""
    if not TMDB_API_KEY:
        logger.error("TMDB API key not configured")
        return {}
    
    try:
        params["api_key"] = TMDB_API_KEY
        params["language"] = "en-US"
        url = f"{TMDB_BASE}{endpoint}"
        
        logger.info(f"TMDB request: {endpoint}")
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        logger.error(f"TMDB timeout: {endpoint}")
        return {}
    except requests.exceptions.RequestException as e:
        logger.error(f"TMDB request error: {e}")
        return {}
    except Exception as e:
        logger.error(f"TMDB unexpected error: {e}")
        return {}

def get_genres_map():
    """Get TMDB genre mapping"""
    data = tmdb_get("/genre/movie/list")
    return {g["name"]: g["id"] for g in data.get("genres", [])}

def get_streaming_providers(movie_id, country="IN"):
    """Get streaming providers for a movie"""
    data = tmdb_get(f"/movie/{movie_id}/watch/providers")
    results = data.get("results", {}).get(country, {})
    providers = []
    
    for ptype in ("flatrate", "free", "ads"):
        for p in results.get(ptype, []):
            name = p.get("provider_name", "")
            logo = p.get("logo_path", "")
            if name and name not in [x["name"] for x in providers]:
                providers.append({
                    "name": name,
                    "logo": f"{TMDB_IMG_SMALL}{logo}" if logo else ""
                })
    return providers[:5]

def get_imdb_id(movie_id):
    """Get IMDB ID for a movie"""
    data = tmdb_get(f"/movie/{movie_id}/external_ids")
    return data.get("imdb_id", "")

def build_movie_obj(m):
    """Build standardized movie object from TMDB data"""
    movie_id = m.get("id")
    poster   = m.get("poster_path", "")
    backdrop = m.get("backdrop_path", "")
    
    return {
        "id":        movie_id,
        "title":     m.get("title", "Unknown"),
        "year":      str(m.get("release_date", ""))[:4] if m.get("release_date") else "",
        "rating":    round(m.get("vote_average", 0), 1),
        "votes":     m.get("vote_count", 0),
        "overview":  m.get("overview", ""),
        "poster":    f"{TMDB_IMG}{poster}" if poster else "",
        "backdrop":  f"{TMDB_IMG}{backdrop}" if backdrop else "",
        "genres":    m.get("genre_ids", []),
        "language":  m.get("original_language", ""),
        "popularity":m.get("popularity", 0),
    }

# ── Health Check Route ───────────────────────────────────────────────
@app.route("/health")
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "gemini_configured": gemini_model is not None,
        "tmdb_configured": TMDB_API_KEY is not None
    })

# ── Routes ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Render main page"""
    try:
        return render_template("index.html")
    except Exception as e:
        logger.error(f"Error rendering index: {e}")
        return f"Error loading page: {str(e)}", 500

@app.route("/api/trending")
@handle_errors
def trending():
    """Get trending movies"""
    media  = request.args.get("media", "movie")
    window = request.args.get("window", "week")
    
    data   = tmdb_get(f"/trending/{media}/{window}")
    if not data:
        return jsonify({"error": "Failed to fetch trending movies", "movies": []}), 500
    
    movies = [build_movie_obj(m) for m in data.get("results", [])[:12]]
    return jsonify({"movies": movies})

@app.route("/api/search")
@handle_errors
def search():
    """Search for movies"""
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"movies": []})
    
    data   = tmdb_get("/search/movie", query=query, page=1)
    if not data:
        return jsonify({"error": "Search failed", "movies": []}), 500
    
    movies = [build_movie_obj(m) for m in data.get("results", [])[:10]]
    return jsonify({"movies": movies})

@app.route("/api/movie/<int:movie_id>")
@handle_errors
def movie_detail(movie_id):
    """Get detailed movie information"""
    data = tmdb_get(f"/movie/{movie_id}", append_to_response="credits,videos")
    if not data or not data.get("id"):
        return jsonify({"error": "Movie not found"}), 404
    
    providers = get_streaming_providers(movie_id)
    imdb_id   = get_imdb_id(movie_id)

    # Trailer
    trailer_key = ""
    for v in data.get("videos", {}).get("results", []):
        if v.get("type") == "Trailer" and v.get("site") == "YouTube":
            trailer_key = v.get("key", "")
            break

    # Cast
    cast = []
    for c in data.get("credits", {}).get("cast", [])[:6]:
        profile = c.get("profile_path", "")
        cast.append({
            "name":      c.get("name", ""),
            "character": c.get("character", ""),
            "photo":     f"{TMDB_IMG_SMALL}{profile}" if profile else ""
        })

    poster   = data.get("poster_path", "")
    backdrop = data.get("backdrop_path", "")

    return jsonify({
        "id":          movie_id,
        "title":       data.get("title", ""),
        "tagline":     data.get("tagline", ""),
        "overview":    data.get("overview", ""),
        "year":        str(data.get("release_date", ""))[:4] if data.get("release_date") else "",
        "runtime":     data.get("runtime", 0),
        "rating":      round(data.get("vote_average", 0), 1),
        "votes":       data.get("vote_count", 0),
        "genres":      [g["name"] for g in data.get("genres", [])],
        "poster":      f"{TMDB_IMG}{poster}" if poster else "",
        "backdrop":    f"{TMDB_IMG}{backdrop}" if backdrop else "",
        "imdb_id":     imdb_id,
        "imdb_url":    f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else "",
        "trailer":     f"https://www.youtube.com/watch?v={trailer_key}" if trailer_key else "",
        "providers":   providers,
        "cast":        cast,
        "language":    data.get("original_language", ""),
        "budget":      data.get("budget", 0),
        "revenue":     data.get("revenue", 0),
    })

@app.route("/api/recommend", methods=["POST"])
@handle_errors
def recommend():
    """Generate AI-powered movie recommendations"""
    prefs = request.json or {}
    
    if not TMDB_API_KEY:
        return jsonify({"error": "TMDB API not configured"}), 503

    genres_map = get_genres_map()

    # Build TMDB discover params
    params = {
        "sort_by":        "vote_average.desc",
        "vote_count.gte": 80,
        "page":           1,
    }

    # Map genre
    genre_map = {
        "Action":    "Action",
        "Comedy":    "Comedy",
        "Horror":    "Horror",
        "Sci-Fi":    "Science Fiction",
        "Romance":   "Romance",
        "Thriller":  "Thriller",
        "Drama":     "Drama",
        "Fantasy":   "Adventure",
        "Animation": "Animation",
    }
    gname = genre_map.get(prefs.get("genre", ""), "")
    if gname and gname in genres_map:
        params["with_genres"] = genres_map[gname]

    # Map language
    lang_map = {
        "English": "en", "Hindi": "hi", "Telugu": "te",
        "Tamil":   "ta", "Korean":"ko", "Spanish": "es",
        "French":  "fr", "Japanese":"ja",
    }
    lang_code = lang_map.get(prefs.get("language", ""), "")
    if lang_code:
        params["with_original_language"] = lang_code

    # Filter by era
    era = prefs.get("era", "")
    if era == "2020-2024":
        params["primary_release_date.gte"] = "2020-01-01"
        params["primary_release_date.lte"] = "2024-12-31"
    elif era == "2010s":
        params["primary_release_date.gte"] = "2010-01-01"
        params["primary_release_date.lte"] = "2019-12-31"
    elif era == "classics":
        params["primary_release_date.lte"] = "2009-12-31"

    # Get movies from TMDB
    data   = tmdb_get("/discover/movie", **params)
    movies = data.get("results", [])

    # Fallback to trending if no results
    if not movies:
        logger.info("No discover results, falling back to trending")
        data   = tmdb_get("/trending/movie/week")
        movies = data.get("results", [])

    if not movies:
        return jsonify({"error": "No movies found", "movies": [], "prefs": prefs}), 404

    # Try AI ranking if Gemini is available
    ai_results = []
    if gemini_model:
        try:
            movie_list = "\n".join([
                f"- {m.get('title','?')} ({str(m.get('release_date',''))[:4]}) "
                f"Rating:{m.get('vote_average',0):.1f} "
                f"Overview:{str(m.get('overview',''))[:100]}"
                for m in movies[:20]
            ])

            ai_prompt = f"""
User Preferences:
Genre: {prefs.get('genre','Any')} | Sub-genre: {prefs.get('subGenre','Any')}
Language: {prefs.get('language','Any')} | Mood: {prefs.get('mood','Any')}
Viewing with: {prefs.get('context','Solo')} | Era: {prefs.get('era','Any')}
Favorites: {prefs.get('favorites','Not specified')}

TMDB Movies Pool:
{movie_list}

Return ONLY a valid JSON array (no markdown) of top 6 picks:
[{{"rank":1,"title":"exact movie title","reason":"2-sentence personalized reason","mood_match":"92%","tag":"Must Watch"}}]
Tags options: "Must Watch", "Hidden Gem", "Crowd Pleaser", "Deep Cut", "Feel Good", "Mind Bender"
"""

            chat = gemini_model.start_chat()
            resp = chat.send_message(ai_prompt)
            text = resp.text.strip()
            # Strip code fences
            text = re.sub(r"```json|```", "", text).strip()
            ai_results = json.loads(text)
            logger.info(f"AI generated {len(ai_results)} recommendations")
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            ai_results = []

    # Match AI titles to TMDB data
    final = []
    if ai_results:
        for ai in ai_results:
            for m in movies:
                if m.get("title", "").lower() == ai["title"].lower():
                    obj = build_movie_obj(m)
                    obj["ai_reason"]    = ai.get("reason", "")
                    obj["mood_match"]   = ai.get("mood_match", "")
                    obj["tag"]          = ai.get("tag", "")
                    obj["rank"]         = ai.get("rank", len(final)+1)
                    final.append(obj)
                    break

    # Pad with top TMDB results if AI didn't match enough
    used_ids = {m["id"] for m in final}
    for m in sorted(movies, key=lambda x: x.get("vote_average",0), reverse=True):
        if m.get("id") not in used_ids and len(final) < 6:
            obj = build_movie_obj(m)
            obj["ai_reason"]  = "Highly rated match for your preferences."
            obj["mood_match"] = ""
            obj["tag"]        = "Top Rated"
            obj["rank"]       = len(final) + 1
            final.append(obj)

    return jsonify({"movies": final, "prefs": prefs})

@app.route("/api/chat", methods=["POST"])
@handle_errors
def chat():
    """AI chat endpoint"""
    body    = request.json or {}
    message = body.get("message", "").strip()
    history = body.get("history", [])

    if not message:
        return jsonify({"reply": "Please ask me something!"})

    if not gemini_model:
        return jsonify({
            "reply": "AI chat is currently unavailable. Please check your API configuration."
        }), 503

    # Build Gemini chat history
    chat_history = []
    for h in history[-6:]:  # last 6 turns
        chat_history.append({"role": h["role"], "parts": [h["text"]]})

    # Also search TMDB if movie-related
    tmdb_context = ""
    search_triggers = ["find", "recommend", "suggest", "best", "top", "watch", "movie", "film", "show"]
    if any(t in message.lower() for t in search_triggers):
        results = tmdb_get("/search/movie", query=message[:60])
        if results.get("results"):
            top3 = results["results"][:3]
            tmdb_context = "\n\nRelevant TMDB results: " + ", ".join([
                f"{m.get('title','?')} ({str(m.get('release_date',''))[:4]}, ⭐{m.get('vote_average',0):.1f})"
                for m in top3
            ])

    try:
        chat_obj = gemini_model.start_chat(history=chat_history)
        full_msg = message + tmdb_context
        resp     = chat_obj.send_message(full_msg)
        reply    = resp.text
    except Exception as e:
        logger.error(f"Chat error: {e}")
        reply = f"I'm having trouble connecting right now. Please try again!"

    return jsonify({"reply": reply})

@app.route("/api/genres")
@handle_errors
def genres():
    """Get list of movie genres"""
    data = tmdb_get("/genre/movie/list")
    return jsonify({"genres": data.get("genres", [])})

# ── Error Handlers ───────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    return jsonify({"error": "Internal server error"}), 500

# ── Main ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"Starting CineMatch AI on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)

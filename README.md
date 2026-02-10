# 🎬 CineMatch AI - Your Personal Movie Recommendation Engine

A production-ready full-stack web application powered by Flask, Google Gemini AI, and The Movie Database (TMDB) API.

## ✨ Features

- **AI-Powered Recommendations**: Personalized movie suggestions using Google Gemini AI
- **Smart Movie Search**: Real-time search across TMDB's extensive movie database
- **Detailed Movie Info**: Cast, ratings, streaming providers, trailers, and more
- **Trending Movies**: Stay updated with the latest trending films
- **Interactive Chat**: Conversational AI for movie discussions and recommendations
- **Beautiful UI**: Modern, responsive design with cinematic aesthetics

## 🚀 Quick Deploy to Render.com

### Prerequisites
- A Render.com account (free tier works)
- TMDB API Key (get it free from [TMDB](https://www.themoviedb.org/settings/api))
- Google Gemini API Key (get it free from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Deployment Steps

1. **Fork/Clone this repository**

2. **Connect to Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab repository

3. **Configure Environment Variables**
   In Render dashboard, add these environment variables:
   
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   TMDB_API_KEY=your_tmdb_api_key_here
   SECRET_KEY=auto_generated_by_render
   ```

4. **Deploy**
   - Render will automatically detect the `render.yaml` and deploy
   - Wait for build to complete (~3-5 minutes)
   - Your app will be live at `https://your-app-name.onrender.com`

## 🛠️ Local Development

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd cinematch-ai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your_key_here"
export TMDB_API_KEY="your_key_here"
export SECRET_KEY="your_secret_key"

# Run the app
python app.py
```

Visit `http://localhost:5000` in your browser.

## 📁 Project Structure

```
cinematch-ai/
├── app.py                 # Flask application (main backend)
├── templates/
│   └── index.html        # Frontend (HTML, CSS, JS all-in-one)
├── requirements.txt      # Python dependencies
├── render.yaml          # Render.com deployment config
├── runtime.txt          # Python version specification
├── Procfile            # Process configuration
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini AI API key for recommendations |
| `TMDB_API_KEY` | Yes | The Movie Database API key |
| `SECRET_KEY` | Yes | Flask secret key (auto-generated on Render) |
| `PORT` | No | Port to run the app (default: 5000) |
| `FLASK_ENV` | No | Environment mode (production/development) |

## 🐛 Troubleshooting

### Internal Server Error

If you see "Internal Server Error" after deployment:

1. **Check Environment Variables**
   - Ensure `GEMINI_API_KEY` and `TMDB_API_KEY` are set correctly in Render
   - Variables should NOT have quotes around them

2. **Check Logs**
   - Go to Render Dashboard → Your Service → Logs
   - Look for error messages (usually at startup)

3. **Verify API Keys**
   - Test your TMDB key: `curl "https://api.themoviedb.org/3/movie/550?api_key=YOUR_KEY"`
   - Test your Gemini key in [AI Studio](https://makersuite.google.com/)

4. **Common Issues**
   - **Missing API Keys**: App will start but API calls will fail
   - **Invalid API Keys**: Check for extra spaces or incorrect keys
   - **Rate Limits**: Free tier has limits - wait and retry

### Health Check

Visit `/health` endpoint to check service status:
```
https://your-app.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "gemini_configured": true,
  "tmdb_configured": true
}
```

## 🔒 Security Notes

- **Never commit API keys** to version control
- Use environment variables for all sensitive data
- The `.gitignore` file protects `.env` files
- Render automatically generates a secure `SECRET_KEY`

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/health` | GET | Health check endpoint |
| `/api/trending` | GET | Get trending movies |
| `/api/search?q=query` | GET | Search movies |
| `/api/movie/<id>` | GET | Get movie details |
| `/api/recommend` | POST | Get AI recommendations |
| `/api/chat` | POST | Chat with AI |
| `/api/genres` | GET | Get genre list |

## 🎨 Tech Stack

- **Backend**: Flask (Python)
- **AI**: Google Gemini 1.5 Flash
- **Data**: TMDB API
- **Deployment**: Render.com
- **Server**: Gunicorn
- **Frontend**: Vanilla JavaScript, CSS3

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 💬 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Review Render logs for error details
3. Verify your API keys are valid and have quota
4. Open an issue with error details

## 🌟 Acknowledgments

- [TMDB](https://www.themoviedb.org/) for the comprehensive movie database
- [Google Gemini](https://ai.google.dev/) for AI-powered recommendations
- [Render.com](https://render.com/) for easy deployment

---

Made with ❤️ for movie lovers everywhere

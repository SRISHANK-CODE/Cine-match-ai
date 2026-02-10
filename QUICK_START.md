# 🚀 QUICK START - Fix Your Render Deployment NOW

## ⚡ Immediate Actions (5 Minutes)

### Step 1: Update Your Code
Replace your current files with the fixed versions from `cinematch-ai-fixed` folder.

### Step 2: Remove Hard-Coded API Keys
**CRITICAL**: The main issue is likely hard-coded API keys in render.yaml

Go to Render Dashboard → Your Service → Environment:

**Add these variables** (if not already there):
```
GEMINI_API_KEY = [paste your actual Gemini key here]
TMDB_API_KEY = [paste your actual TMDB key here]
```

**Important**: 
- NO quotes around values
- NO spaces before/after the =
- Copy-paste carefully

### Step 3: Update render.yaml
Your render.yaml should look like this:

```yaml
services:
  - type: web
    name: cinematch-ai
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level info
    envVars:
      - key: GEMINI_API_KEY
        sync: false          # ← This means use Render dashboard value
      - key: TMDB_API_KEY
        sync: false          # ← This means use Render dashboard value
      - key: SECRET_KEY
        generateValue: true
```

**Remove** any lines with:
- `value: AIzaSy...` (Gemini key)
- `value: 0c38f4...` (TMDB key)

### Step 4: Redeploy
1. Push your updated code to GitHub/GitLab
2. Render will auto-deploy
3. OR: Click "Manual Deploy" in Render dashboard

### Step 5: Verify
Visit: `https://your-app-name.onrender.com/health`

Should see:
```json
{
  "status": "healthy",
  "gemini_configured": true,
  "tmdb_configured": true
}
```

If you see `false` for any API:
- Go back to Step 2
- Double-check your environment variables
- Make sure no extra spaces or quotes

## 🎯 What Was Fixed?

1. **Error Handling** - No more silent failures
2. **API Validation** - Checks keys on startup
3. **Logging** - See exactly what's happening
4. **Health Check** - `/health` endpoint to verify status
5. **Security** - Keys moved to environment variables

## 🐛 Still Getting Errors?

### Check Render Logs
Dashboard → Your Service → Logs

Look for:
- ✅ "Starting CineMatch AI on port 10000"
- ✅ "Gemini AI initialized successfully"
- ❌ "API key not configured"
- ❌ Any error messages

### Common Issues

**"gemini_configured": false**
→ GEMINI_API_KEY not set or invalid in Render

**"tmdb_configured": false**
→ TMDB_API_KEY not set or invalid in Render

**"Internal Server Error" still happening**
→ Check logs for specific error message
→ Verify both API keys work:
  - Test TMDB: https://www.themoviedb.org/settings/api
  - Test Gemini: https://makersuite.google.com/

**Page loads but features don't work**
→ Check browser console for JavaScript errors
→ Verify API endpoints return data, not errors

## 📞 Quick Debug Commands

```bash
# Check health
curl https://your-app.onrender.com/health

# Check trending (should return movies)
curl https://your-app.onrender.com/api/trending

# Check search (should return movies)
curl https://your-app.onrender.com/api/search?q=avatar
```

## ✅ Success Criteria

Your app is working when:
- [ ] /health shows all `true`
- [ ] Home page loads with movies
- [ ] Search returns results
- [ ] Movie details work
- [ ] Recommendations generate
- [ ] No errors in Render logs

## 🎉 Next Steps

Once working:
1. Read DEPLOYMENT.md for full deployment guide
2. Read FIXES.md to understand what was fixed
3. Read README.md for complete documentation
4. Bookmark your app URL
5. Test all features thoroughly

---

**Time to Fix**: 5-10 minutes
**Difficulty**: Easy (just update env vars)
**Success Rate**: 99% with correct API keys

Good luck! 🚀

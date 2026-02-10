# 🚀 CineMatch AI - Deployment Checklist

## ✅ Pre-Deployment Checklist

### 1. API Keys Setup
- [ ] Get TMDB API Key from https://www.themoviedb.org/settings/api
- [ ] Get Google Gemini API Key from https://makersuite.google.com/app/apikey
- [ ] Test both API keys to ensure they work

### 2. Render.com Setup
- [ ] Create a free account at https://render.com
- [ ] Verify email address
- [ ] Connect GitHub/GitLab account

### 3. Code Repository
- [ ] Push all code to GitHub/GitLab
- [ ] Verify all files are present:
  - [ ] app.py
  - [ ] requirements.txt
  - [ ] render.yaml
  - [ ] runtime.txt
  - [ ] Procfile
  - [ ] templates/index.html
  - [ ] README.md
  - [ ] .gitignore

## 📋 Deployment Steps

### Step 1: Create New Web Service
1. Go to Render Dashboard
2. Click "New +" button
3. Select "Web Service"
4. Connect your repository

### Step 2: Configure Service
1. **Name**: `cinematch-ai` (or your preferred name)
2. **Region**: Choose closest to your users
3. **Branch**: `main` or `master`
4. **Runtime**: Python 3
5. **Build Command**: Auto-detected from render.yaml
6. **Start Command**: Auto-detected from render.yaml

### Step 3: Set Environment Variables
Go to "Environment" tab and add:

```
GEMINI_API_KEY = your_actual_gemini_key_here
TMDB_API_KEY = your_actual_tmdb_key_here
SECRET_KEY = (leave empty - auto-generated)
```

**IMPORTANT**: 
- Do NOT include quotes around the values
- Do NOT commit these to Git
- Copy-paste carefully to avoid spaces

### Step 4: Deploy
1. Click "Create Web Service"
2. Wait for build (3-5 minutes)
3. Watch the logs for any errors

### Step 5: Verify Deployment
1. Visit your app URL: `https://your-app-name.onrender.com`
2. Check health endpoint: `https://your-app-name.onrender.com/health`
3. Test trending movies feature
4. Test search functionality
5. Try getting recommendations

## 🐛 Common Issues & Solutions

### Issue: "Internal Server Error"

**Cause 1: Missing Environment Variables**
- Solution: Add GEMINI_API_KEY and TMDB_API_KEY in Render dashboard
- Verify in Logs: Look for "API key not configured" messages

**Cause 2: Invalid API Keys**
- Solution: Test your keys:
  ```bash
  # Test TMDB
  curl "https://api.themoviedb.org/3/movie/550?api_key=YOUR_KEY"
  
  # Test Gemini at https://makersuite.google.com/
  ```

**Cause 3: Build Failed**
- Solution: Check Render logs for Python dependency errors
- Verify requirements.txt has correct package versions

### Issue: App Starts but Features Don't Work

**Symptoms**: Health check shows `false` for APIs
- Check: Environment variables are set correctly
- Check: No extra spaces or quotes in variable values
- Check: API keys have proper permissions enabled

### Issue: Slow Response Times

**Expected**: First request after idle may take 30+ seconds (free tier)
- Render free tier spins down after inactivity
- Subsequent requests will be fast
- Consider upgrading to paid tier for always-on service

### Issue: Rate Limits

- TMDB: 40 requests per 10 seconds
- Gemini: Free tier has daily limits
- Solution: Wait and retry, or upgrade API plans

## 📊 Post-Deployment Monitoring

### Check Logs Regularly
```
Render Dashboard → Your Service → Logs
```

Look for:
- ✅ "Starting CineMatch AI on port 10000"
- ✅ "Gemini AI initialized successfully"
- ❌ Any error messages or exceptions

### Test All Features
- [ ] Home page loads
- [ ] Trending movies display
- [ ] Search works
- [ ] Movie details load
- [ ] Recommendations generate
- [ ] AI chat responds
- [ ] Streaming providers show

### Performance Monitoring
- First load: ~30 seconds (cold start)
- Subsequent loads: <2 seconds
- API requests: <5 seconds

## 🔄 Updates & Maintenance

### Updating Your App
1. Push changes to your Git repository
2. Render will auto-deploy (if enabled)
3. Or manually trigger deploy in Render dashboard

### Rotating API Keys
1. Generate new keys in respective platforms
2. Update environment variables in Render
3. Restart service

### Checking Health
Regular health checks:
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "gemini_configured": true,
  "tmdb_configured": true
}
```

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ Health endpoint returns all `true` values
- ✅ Home page loads with trending movies
- ✅ Search returns results
- ✅ Movie details page works
- ✅ AI recommendations generate
- ✅ Chat feature responds
- ✅ No errors in Render logs

## 📞 Need Help?

If you're still having issues:

1. **Check Logs First**: Most issues are visible in logs
2. **Verify Environment Variables**: 90% of issues are here
3. **Test API Keys**: Ensure they work outside the app
4. **Review This Checklist**: Did you miss a step?

## 🎉 Success!

Once everything is working:
- [ ] Bookmark your app URL
- [ ] Share with friends
- [ ] Star the GitHub repository
- [ ] Leave feedback

---

**Remember**: The free tier on Render:
- Spins down after 15 minutes of inactivity
- Has a 750-hour/month limit (enough for personal use)
- May have cold starts (30+ second first load)
- Perfect for demos and personal projects

For production use, consider upgrading to a paid plan for:
- Always-on service
- Faster performance
- More resources
- Better reliability

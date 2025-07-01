# Brainwave Deployment Guide

This guide covers deploying the Brainwave speech transcription app to various cloud platforms. The app now includes persistent data storage for audio recordings and transcripts.

## Prerequisites

- OpenAI API key
- Git repository set up
- Python 3.9+ and dependencies listed in `requirements.txt`

## Quick Deploy

Use the deployment helper script:

```bash
python deploy.py
```

This will guide you through deploying to your preferred platform and help set up all required configurations.

## Platform-Specific Instructions

### 1. Railway (Recommended) ⭐

Railway provides persistent storage, automatic HTTPS, and easy environment variable management - perfect for Brainwave's data collection features.

**Quick Deploy:**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy (or use deploy.py script)
python deploy.py
```

**Manual Deployment:**
```bash
railway project new brainwave
railway up
```

**Set Environment Variables:**
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Find your "brainwave" project
3. Go to **Variables** tab
4. Add these variables:
   - `OPENAI_API_KEY`: `your-openai-api-key-here`
   - `BRAINWAVE_DATA_DIR`: `/app/brainwave-data`

**Files used:**
- `railway.toml` - Railway configuration with optimized settings
- `Procfile` - Start command configuration

**Benefits:**
- ✅ Automatic HTTPS (microphone access works)
- ✅ Persistent file storage (data saved between deployments)
- ✅ Easy environment variable management
- ✅ Automatic domain assignment

### 2. Render

Render provides persistent storage and is production-ready with automatic HTTPS.

**Steps:**
1. Create account at [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new **Web Service**
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn realtime_server:app --host 0.0.0.0 --port $PORT --log-level info`
   - **Environment:** Python 3
   - **Instance Type:** Starter (free tier available)
5. Add environment variables:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `BRAINWAVE_DATA_DIR`: `/opt/render/project/src/brainwave-data`

**Benefits:**
- ✅ Automatic HTTPS
- ✅ Persistent file storage
- ✅ Free tier available
- ✅ Good for production use

### 3. Vercel

Vercel is fast but doesn't support persistent file storage (data is temporary).

**Quick Deploy:**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod

# Add environment variable
vercel env add OPENAI_API_KEY
```

**Configuration:**
- `vercel.json` is already configured
- Data saving features work temporarily but files are lost between deployments

**Limitations:**
- ❌ No persistent storage (data lost on redeployment)
- ✅ Automatic HTTPS
- ✅ Very fast deployment

### 4. Heroku

**Steps:**
1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-brainwave-app`
4. Set environment variable: `heroku config:set OPENAI_API_KEY=your-key`
5. Deploy: `git push heroku main`

**Limitations:**
- ❌ Files lost on dyno restarts (every 24 hours)
- ✅ Automatic HTTPS

## Local Development with HTTPS

For local testing with microphone access:

```bash
python run_https.py
```

**What this does:**
- Generates self-signed SSL certificates
- Starts server at `https://localhost:3005`
- Enables microphone access in browsers
- Shows clear instructions for bypassing browser security warnings

**Updated Features:**
- ✅ Clear URL instructions (use `localhost:3005`, not `0.0.0.0:3005`)
- ✅ Better error messages for missing API keys
- ✅ Automatic certificate generation

## Environment Variables

All platforms need these environment variables:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | None | **Yes** |
| `BRAINWAVE_DATA_DIR` | Directory for saved audio/transcripts | `./brainwave-data` | No |
| `PORT` | Server port (set automatically by platforms) | `3005` | Platform-dependent |

## Testing Your Deployment

### 1. Basic Functionality
1. Visit your deployed URL (should use HTTPS)
2. Click **"Start Recording"** - browser should request microphone permission
3. Grant microphone access
4. Speak something clearly and wait for transcription
5. Verify the transcribed text appears

### 2. Data Persistence (Railway/Render only)
1. After recording, visit `https://your-app-url.com/api/v1/sessions`
2. You should see your session data with:
   - Timestamp directory name
   - File list (audio.wav, transcript.txt, meta.json)
   - File sizes confirming data was saved

### 3. Multiple Sessions
1. Record multiple different sessions
2. Check `/api/v1/sessions` again
3. Verify each session creates a new timestamped directory

## Data Storage Details

The app automatically saves session data in timestamped directories:

```
brainwave-data/
├── 2025-01-01_14-41-59/
│   ├── audio.wav      # 24kHz mono audio (resampled from 48kHz)
│   ├── transcript.txt # Final transcribed text
│   └── meta.json     # Session metadata (duration, word count, etc.)
├── 2025-01-01_15-23-17/
│   ├── audio.wav
│   ├── transcript.txt
│   └── meta.json
└── ... (more sessions)
```

**Session Metadata (meta.json) includes:**
- Start/end timestamps
- Session duration
- Number of audio chunks processed
- Transcript length and word count
- Audio processing statistics

## Troubleshooting

### Microphone Access Blocked
- **Issue**: Browser shows "Microphone blocked" or doesn't request permission
- **Solution**: Ensure your site uses HTTPS (all recommended platforms provide this)
- **Local testing**: Use `python run_https.py`, not regular HTTP server

### OpenAI API Connection Issues
- **Issue**: "OPENAI_API_KEY is not set" or connection errors
- **Solution**: 
  - Verify API key is set in platform's environment variables
  - Check API key is valid at [OpenAI dashboard](https://platform.openai.com/api-keys)
  - Ensure no extra spaces or quotes in the API key

### Data Saving Issues
- **Issue**: `/api/v1/sessions` shows empty or no data
- **Check**: Platform supports persistent storage (Railway ✅, Render ✅, Vercel ❌, Heroku ❌)
- **Verify**: `BRAINWAVE_DATA_DIR` path is writable
- **Test**: Run locally with `python run_https.py` first

### Build/Deployment Failures
- **Railway**: Check build logs in dashboard, ensure all files are committed to git
- **Render**: Verify Python version and requirements.txt is complete
- **Common fixes**:
  - Commit all changes: `git add . && git commit -m "Deploy"`
  - Check requirements.txt includes all dependencies
  - Ensure Python 3.9+ compatibility

### "PosixPath object has no attribute 'write'" Error
- **Fixed**: This was a bug in earlier versions, now resolved
- **If you see this**: Update to latest code version

## Performance Optimization

For production deployments:

1. **Railway**: Use Pro plan for better performance and uptime
2. **Render**: Consider paid plans for faster instance startup
3. **Monitor**: Check `/api/v1/sessions` periodically to ensure data is being saved
4. **Logs**: Monitor platform logs for any WebSocket connection issues

## Security Considerations

- ✅ All platforms provide HTTPS automatically
- ✅ API keys are stored securely in environment variables
- ✅ No sensitive data is logged to console
- ✅ Self-signed certificates for local development only

---

**Recommended Flow:**
1. Test locally with `python run_https.py`
2. Deploy to Railway using `python deploy.py`
3. Set environment variables in Railway dashboard
4. Test microphone access and data saving
5. Use `/api/v1/sessions` to verify data persistence 
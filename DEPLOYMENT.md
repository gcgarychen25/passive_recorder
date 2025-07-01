# Brainwave Deployment Guide

## Local Development with HTTPS

### Quick Start (Recommended)
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-api-key-here"

# Run with HTTPS (solves microphone access issues)
python run_https.py
```

Visit: `https://localhost:3005` (accept the security warning)

### Manual HTTPS Setup
```bash
# Generate SSL certificates
mkdir certs
openssl req -x509 -newkey rsa:4096 -nodes -out certs/cert.pem -keyout certs/key.pem -days 365 -subj "/C=US/ST=Local/L=Local/O=Brainwave/OU=Dev/CN=localhost"

# Run with SSL
uvicorn realtime_server:app --host 0.0.0.0 --port 3005 --ssl-keyfile certs/key.pem --ssl-certfile certs/cert.pem
```

---

## Cloud Deployment Options

### Option 1: Railway (Recommended)
**Pros**: Free tier, automatic HTTPS, persistent storage, easy setup
**Best for**: Personal use, development

1. **Setup**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway init
   railway up
   ```

2. **Set Environment Variables** in Railway dashboard:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `BRAINWAVE_DATA_DIR`: `/app/data` (optional)

3. **Your app will be live at**: `https://your-app.railway.app`

### Option 2: Render
**Pros**: Free tier, simple deployment, automatic HTTPS
**Best for**: Production apps

1. **Fork this repository** on GitHub
2. **Connect to Render**:
   - Go to [render.com](https://render.com)
   - Create new "Web Service"
   - Connect your GitHub repo
   - Use these settings:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn realtime_server:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key

### Option 3: Vercel
**Pros**: Fast deployments, good for frontend-heavy apps
**Cons**: Limited backend support, no persistent storage

1. **Deploy**:
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Deploy
   vercel
   ```

2. **Set Environment Variables**:
   ```bash
   vercel env add OPENAI_API_KEY
   ```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `BRAINWAVE_DATA_DIR` | ❌ No | `brainwave-data` | Directory for storing recordings |

---

## Data Persistence

### Local Development
- Data saved to `brainwave-data/` directory
- Each session creates timestamped folder
- Files: `audio.wav`, `transcript.txt`, `meta.json`

### Cloud Deployment
- **Railway**: Persistent storage included
- **Render**: Limited persistent storage on free tier
- **Vercel**: No persistent storage (sessions lost on restart)

For long-term data retention, consider Railway or Render.

---

## Troubleshooting

### Microphone Access Issues
- **Problem**: Browser blocks microphone access
- **Solution**: Use HTTPS (run `python run_https.py` locally)
- **Why**: Modern browsers require HTTPS for microphone access

### WebSocket Connection Issues
- **Problem**: WebSocket fails to connect
- **Solution**: Check if your deployment platform supports WebSockets
- **Note**: All recommended platforms support WebSockets

### Missing Audio Data
- **Problem**: No audio files saved
- **Solution**: Check `BRAINWAVE_DATA_DIR` permissions and disk space

---

## Quick Deployment Comparison

| Platform | Free Tier | Setup Time | Persistent Storage | Custom Domain |
|----------|-----------|------------|-------------------|---------------|
| Railway | ✅ $5/month | 2 minutes | ✅ Yes | ✅ Yes |
| Render | ✅ Yes | 3 minutes | ⚠️ Limited | ✅ Yes |
| Vercel | ✅ Yes | 1 minute | ❌ No | ✅ Yes |

**Recommendation**: Start with Railway for the best balance of features and ease of use. 
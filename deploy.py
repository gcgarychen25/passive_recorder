#!/usr/bin/env python3
"""
Simple deployment script for Brainwave
Helps you deploy to various cloud platforms quickly.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if required files exist"""
    required_files = ["realtime_server.py", "requirements.txt", "static/"]
    missing = []
    
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print(f"❌ Missing required files: {', '.join(missing)}")
        return False
    
    return True

def check_api_key():
    """Check if OpenAI API key is set"""
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set in environment")
        print("   You'll need to set this in your deployment platform")
        return False
    return True

def deploy_railway():
    """Deploy to Railway"""
    print("🚂 Deploying to Railway...")
    
    try:
        # Check if railway CLI is installed
        subprocess.run(["railway", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Railway CLI not found.")
        print("   Install it with: npm install -g @railway/cli")
        return False
    
    try:
        # Initialize and deploy
        subprocess.run(["railway", "login"], check=True)
        subprocess.run(["railway", "init"], check=True)
        subprocess.run(["railway", "up"], check=True)
        
        print("✅ Deployed to Railway!")
        print("🔧 Don't forget to set OPENAI_API_KEY in Railway dashboard")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Railway deployment failed: {e}")
        return False

def deploy_vercel():
    """Deploy to Vercel"""
    print("▲ Deploying to Vercel...")
    
    try:
        # Check if vercel CLI is installed
        subprocess.run(["vercel", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Vercel CLI not found.")
        print("   Install it with: npm install -g vercel")
        return False
    
    try:
        # Deploy
        subprocess.run(["vercel"], check=True)
        
        print("✅ Deployed to Vercel!")
        print("🔧 Set environment variable: vercel env add OPENAI_API_KEY")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Vercel deployment failed: {e}")
        return False

def show_manual_options():
    """Show manual deployment options"""
    print("\n📋 Manual Deployment Options:")
    print("\n1. **Render** (Recommended for production):")
    print("   - Go to https://render.com")
    print("   - Create new 'Web Service'")
    print("   - Connect your GitHub repo")
    print("   - Build: pip install -r requirements.txt")
    print("   - Start: uvicorn realtime_server:app --host 0.0.0.0 --port $PORT")
    print("   - Set OPENAI_API_KEY environment variable")
    
    print("\n2. **Heroku**:")
    print("   - Create Procfile: web: uvicorn realtime_server:app --host=0.0.0.0 --port=${PORT:-5000}")
    print("   - git push heroku main")
    print("   - heroku config:set OPENAI_API_KEY=your-key")

def main():
    print("🚀 Brainwave Deployment Helper\n")
    
    if not check_requirements():
        sys.exit(1)
    
    check_api_key()
    
    print("Choose deployment platform:")
    print("1. Railway (recommended - persistent storage)")
    print("2. Vercel (fast - no persistent storage)")
    print("3. Show manual options")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        deploy_railway()
    elif choice == "2":
        deploy_vercel()
    elif choice == "3":
        show_manual_options()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main() 
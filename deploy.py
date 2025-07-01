#!/usr/bin/env python3
"""
Interactive deployment helper for Brainwave
"""

import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required tools are installed"""
    tools = {
        'railway': 'npm install -g @railway/cli',
        'vercel': 'npm install -g vercel',
        'git': 'Install from https://git-scm.com'
    }
    
    missing = []
    for tool, install_cmd in tools.items():
        try:
            subprocess.run([tool, '--version'], capture_output=True, check=True)
            print(f"✅ {tool} is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {tool} is not installed")
            print(f"   Install with: {install_cmd}")
            missing.append(tool)
    
    return len(missing) == 0

def deploy_railway():
    """Deploy to Railway"""
    print("\n🚄 Deploying to Railway...")
    
    # Check if logged in
    try:
        result = subprocess.run(['railway', 'whoami'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Please log in to Railway first:")
            print("  railway login")
            return False
    except Exception as e:
        print(f"Error checking Railway login: {e}")
        return False
    
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("Make sure to set it in Railway dashboard after deployment")
    else:
        print(f"✅ OPENAI_API_KEY found (length: {len(api_key)})")
    
    try:
        # Create or connect to Railway project
        print("Creating/connecting to Railway project...")
        subprocess.run(['railway', 'project', 'new', 'brainwave'], check=False)
        
        # Deploy
        print("Deploying to Railway...")
        result = subprocess.run(['railway', 'up'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployed successfully!")
            print("\n📝 Next steps:")
            print("1. Go to Railway dashboard: https://railway.app/dashboard")
            print("2. Find your 'brainwave' project")
            print("3. Go to Variables tab and set:")
            print("   - OPENAI_API_KEY=your-openai-api-key-here")
            print("   - BRAINWAVE_DATA_DIR=/app/brainwave-data")
            print("4. Your app will be available at the domain shown in Railway dashboard")
            print("5. Test microphone access (should work automatically with HTTPS)")
            
            # Try to get the deployment URL
            try:
                url_result = subprocess.run(['railway', 'domain'], capture_output=True, text=True)
                if url_result.returncode == 0 and url_result.stdout.strip():
                    print(f"\n🌐 Your app URL: {url_result.stdout.strip()}")
            except:
                pass
                
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during Railway deployment: {e}")
        return False
    
    return True

def deploy_vercel():
    """Deploy to Vercel"""
    print("\n⚡ Deploying to Vercel...")
    
    try:
        # Check if logged in
        result = subprocess.run(['vercel', 'whoami'], capture_output=True, text=True)
        if result.returncode != 0:
            print("Please log in to Vercel first:")
            print("  vercel login")
            return False
        
        # Deploy
        result = subprocess.run(['vercel', '--prod'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployed successfully!")
            print("\n📝 Next steps:")
            print("1. Go to Vercel dashboard: https://vercel.com/dashboard")
            print("2. Find your project and go to Settings > Environment Variables")
            print("3. Add: OPENAI_API_KEY=your-openai-api-key-here")
            print("4. Redeploy the project")
            
            # Extract URL from output
            lines = result.stdout.split('\n')
            for line in lines:
                if 'https://' in line and 'vercel.app' in line:
                    print(f"\n🌐 Your app URL: {line.strip()}")
                    break
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during Vercel deployment: {e}")
        return False
    
    return True

def deploy_render():
    """Deploy to Render (manual process)"""
    print("\n🎨 Deploying to Render...")
    print("Render deployment is manual. Follow these steps:")
    print()
    print("1. Go to https://render.com and sign up/login")
    print("2. Connect your GitHub repository")
    print("3. Create a new 'Web Service'")
    print("4. Use these settings:")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: uvicorn realtime_server:app --host 0.0.0.0 --port $PORT")
    print("   - Environment: Python 3")
    print("5. Add environment variables:")
    print("   - OPENAI_API_KEY=your-openai-api-key-here")
    print("   - BRAINWAVE_DATA_DIR=/opt/render/project/src/brainwave-data")
    print("6. Deploy!")
    print()
    print("📖 Full guide: see DEPLOYMENT.md")

def main():
    print("🚀 Brainwave Deployment Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("realtime_server.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    print("Checking deployment tools...")
    if not check_requirements():
        print("\n❌ Please install missing tools and try again")
        sys.exit(1)
    
    print("\nChoose deployment platform:")
    print("1. 🚄 Railway (Recommended - automatic HTTPS)")
    print("2. ⚡ Vercel (Serverless)")
    print("3. 🎨 Render (Manual setup)")
    print("4. 💻 Local HTTPS (for testing)")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        success = deploy_railway()
    elif choice == "2":
        success = deploy_vercel()
    elif choice == "3":
        deploy_render()
        success = True
    elif choice == "4":
        print("\n💻 Starting local HTTPS server...")
        print("Run: python run_https.py")
        success = True
    else:
        print("❌ Invalid choice")
        success = False
    
    if success:
        print("\n🎉 Deployment process completed!")
        print("\n📋 Don't forget to:")
        print("- Set OPENAI_API_KEY in your platform's dashboard")
        print("- Test microphone access")
        print("- Check the /api/v1/sessions endpoint to verify data saving")
    else:
        print("\n❌ Deployment failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Script to run the Brainwave server with HTTPS for microphone access.
Generates self-signed certificates for local development.
"""

import os
import subprocess
import sys
from pathlib import Path
import uvicorn

def generate_self_signed_cert():
    """Generate self-signed SSL certificate for localhost"""
    cert_dir = Path("certs")
    cert_dir.mkdir(exist_ok=True)
    
    cert_file = cert_dir / "cert.pem"
    key_file = cert_dir / "key.pem"
    
    if cert_file.exists() and key_file.exists():
        print("SSL certificates already exist, using existing ones...")
        return str(cert_file), str(key_file)
    
    print("Generating self-signed SSL certificate...")
    
    try:
        # Generate private key and certificate
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:4096", "-nodes",
            "-out", str(cert_file),
            "-keyout", str(key_file),
            "-days", "365",
            "-subj", "/C=US/ST=Local/L=Local/O=Brainwave/OU=Dev/CN=localhost"
        ], check=True, capture_output=True)
        
        print(f"✅ SSL certificate generated:")
        print(f"   Certificate: {cert_file}")
        print(f"   Private Key: {key_file}")
        return str(cert_file), str(key_file)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to generate SSL certificate: {e}")
        print("Make sure OpenSSL is installed: brew install openssl")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ OpenSSL not found. Install it with: brew install openssl")
        sys.exit(1)

def main():
    print("🚀 Starting Brainwave with HTTPS...")
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        print(f"Current environment variables: {list(os.environ.keys())}")
        sys.exit(1)
    else:
        print(f"✅ OPENAI_API_KEY found (length: {len(api_key)})")
    
    # Check data directory
    data_dir = os.getenv("BRAINWAVE_DATA_DIR", "brainwave-data")
    print(f"📁 Data directory: {data_dir}")
    
    # Generate or use existing certificates
    cert_file, key_file = generate_self_signed_cert()
    
    print(f"\n🌐 Open your browser and go to: https://localhost:3005")
    print("⚠️  Your browser will show a security warning for the self-signed certificate.")
    print("   Click 'Advanced' → 'Proceed to localhost (unsafe)' to continue.")
    print("\n🎤 Microphone access should work with HTTPS!")
    print("📝 Note: Uvicorn will show 0.0.0.0:3005 below, but you should use localhost:3005\n")
    
    # Start the server with SSL
    uvicorn.run(
        "realtime_server:app",
        host="0.0.0.0",
        port=3005,
        ssl_keyfile=key_file,
        ssl_certfile=cert_file,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main() 
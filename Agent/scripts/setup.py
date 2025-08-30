#!/usr/bin/env python3
"""
GPAF Setup Script
This script installs all required dependencies for GPAF
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    print("🚀 GPAF Setup - Installing Dependencies...")
    
    # Core dependencies
    core_packages = [
        "flask[async]==3.0.3",
        "flask-basicauth==0.2.0", 
        "python-dotenv==1.1.0",
        "cryptography",
        "a2wsgi==1.10.8",
        "nest-asyncio==1.6.0"
    ]
    
    # AI/ML dependencies
    ai_packages = [
        "openai",
        "anthropic", 
        "google-generativeai",
        "langchain-openai==0.3.11",
        "langchain-anthropic==0.3.3",
        "langchain-community==0.3.19",
        "langchain-groq==0.2.2",
        "langchain-huggingface==0.1.2",
        "sentence-transformers==3.0.1",
        "tiktoken==0.8.0",
        "faiss-cpu==1.11.0"
    ]
    
    # Audio/Media dependencies  
    media_packages = [
        "openai-whisper==20240930",
        "playwright==1.52.0"
    ]
    
    # Utility dependencies
    utility_packages = [
        "docker==7.1.0",
        "paramiko==3.5.0",
        "GitPython==3.1.43",
        "duckduckgo-search==6.1.12",
        "browser-use==0.2.5",
        "fastmcp==2.3.4",
        "mcp==1.9.0"
    ]
    
    all_packages = core_packages + ai_packages + media_packages + utility_packages
    
    success_count = 0
    total_count = len(all_packages)
    
    for package in all_packages:
        if install_package(package):
            success_count += 1
        print()  # Add spacing
    
    print(f"📊 Installation Summary:")
    print(f"   ✅ Success: {success_count}/{total_count}")
    print(f"   ❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("\n🎉 All dependencies installed successfully!")
        print("You can now run GPAF with: python run.py")
    else:
        print(f"\n⚠️ Some dependencies failed to install.")
        print("You can still use Docker: ./docker.sh up")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
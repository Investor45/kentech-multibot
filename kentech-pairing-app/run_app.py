"""
Simple test runner for the Kentech Bot Pairing Application.
"""

import sys
import os
import asyncio

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import main
    
    if __name__ == "__main__":
        print("🚀 Starting Kentech Bot Pairing Application...")
        print("📍 Access points:")
        print("   - API Docs: http://localhost:8000/docs")
        print("   - Health: http://localhost:8000/health")
        print("   - Status: http://localhost:8000/api/status")
        print()
        
        main()
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("🔧 Installing missing dependencies...")
    
    # Try to install missing packages
    import subprocess
    
    packages = [
        "pydantic-settings",
        "aiosqlite", 
        "fastapi",
        "uvicorn",
        "sqlalchemy[asyncio]",
        "loguru",
        "python-dotenv"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {package}")
    
    print("\n🔄 Retrying application start...")
    try:
        from main import main
        main()
    except Exception as retry_error:
        print(f"❌ Still failed: {retry_error}")
        
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    print(f"🔍 Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()

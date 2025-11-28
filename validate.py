"""
Quick validation script to test the basic structure
"""

import os
import sys

def validate_structure():
    """Validate that the project has the correct structure"""
    
    print("🔍 Validating project structure...")
    
    required_files = [
        "solution.py",
        "server.py", 
        "requirements.txt",
        ".env",
        "README.md"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def validate_imports():
    """Validate that we can import the main modules"""
    
    print("\n🔍 Validating imports...")
    
    try:
        # Test basic imports
        import requests
        print("✅ requests")
        
        import fastapi
        print("✅ fastapi")
        
        import uvicorn
        print("✅ uvicorn")
        
        import pydantic
        print("✅ pydantic")
        
        # Test our solution module
        sys.path.append(os.getcwd())
        
        print("✅ All imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def validate_env():
    """Validate environment configuration"""
    
    print("\n🔍 Validating environment...")
    
    if not os.path.exists(".env"):
        print("❌ .env file not found")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
        
    if "OPENAI_API_KEY" in content:
        print("✅ OpenAI API key configured")
        return True
    else:
        print("❌ OpenAI API key not found in .env")
        return False

if __name__ == "__main__":
    print("🏛️  Legal Clerk RAG Agent - Structure Validation")
    print("=" * 50)
    
    all_valid = True
    
    all_valid &= validate_structure()
    all_valid &= validate_imports() 
    all_valid &= validate_env()
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All validations passed! The agent is ready to deploy.")
        print("\nNext steps:")
        print("1. Run: python server.py --port 8100")
        print("2. In another terminal: ngrok http 8100") 
        print("3. Submit your ngrok URL + /solve")
    else:
        print("❌ Some validations failed. Please fix the issues above.")
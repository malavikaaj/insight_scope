#!/usr/bin/env python3
"""
Deployment validation script for InsightScope
Checks if all required dependencies and configurations are in place
"""

import os
import sys
import importlib
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} missing: {filepath}")
        return False

def check_import(module_name, description):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {description}: {module_name}")
        return True
    except ImportError:
        print(f"❌ {description} not available: {module_name}")
        return False

def check_env_file():
    """Check environment configuration"""
    env_path = ".env"
    if not os.path.exists(env_path):
        print(f"⚠️  Environment file not found: {env_path}")
        print("   Create one from .env.production template")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        
    required_vars = ['LLM_PROVIDER', 'EMBEDDING_MODEL', 'VECTOR_DB_PATH']
    missing_vars = []
    
    for var in required_vars:
        if var not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Environment configuration looks good")
        return True

def main():
    """Main validation function"""
    print("🔍 Validating InsightScope deployment configuration...\n")
    
    all_good = True
    
    # Check deployment files
    deployment_files = [
        ("Dockerfile", "Docker configuration"),
        ("docker-compose.yml", "Docker Compose configuration"),
        (".dockerignore", "Docker ignore file"),
        ("deploy.sh", "Deployment script"),
        ("requirements.txt", "Python dependencies"),
        ("DEPLOYMENT.md", "Deployment documentation")
    ]
    
    print("📁 Checking deployment files:")
    for filepath, description in deployment_files:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check application structure
    print("\n📂 Checking application structure:")
    app_structure = [
        ("insight_scope/", "Main application directory"),
        ("insight_scope/app/frontend/app.py", "Streamlit application"),
        ("insight_scope/config/config.py", "Configuration module"),
        ("insight_scope/models/llm/rag_pipeline.py", "RAG pipeline")
    ]
    
    for filepath, description in app_structure:
        if not check_file_exists(filepath, description):
            all_good = False
    
    # Check Python dependencies
    print("\n📦 Checking Python dependencies:")
    dependencies = [
        ("streamlit", "Streamlit framework"),
        ("langchain", "LangChain framework"),
        ("sentence_transformers", "Sentence transformers"),
        ("chromadb", "ChromaDB vector database"),
        ("gpt4all", "GPT4All local LLM"),
        ("dotenv", "Environment variables")
    ]
    
    for module, description in dependencies:
        if not check_import(module, description):
            all_good = False
    
    # Check environment configuration
    print("\n⚙️  Checking environment configuration:")
    if not check_env_file():
        all_good = False
    
    # Check data directories
    print("\n📁 Checking data directories:")
    data_dirs = ["vector_db", "data/processed", "data/raw"]
    for dir_path in data_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"✅ Data directory: {dir_path}")
    
    # Final result
    print("\n" + "="*50)
    if all_good:
        print("🎉 Deployment validation passed!")
        print("   You can now deploy using: ./deploy.sh")
    else:
        print("❌ Deployment validation failed!")
        print("   Please fix the issues above before deploying")
        sys.exit(1)

if __name__ == "__main__":
    main()
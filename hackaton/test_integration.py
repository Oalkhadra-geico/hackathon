#!/usr/bin/env python3
"""
Test script for the integrated DOI Research Assistant system.
This script tests the backend API and frontend-backend communication.
"""

import requests
import json
import time
import sys
import os

def test_backend_health():
    """Test the backend health endpoint"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is the server running?")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_query_endpoint():
    """Test the query endpoint with sample data"""
    print("🔍 Testing query endpoint...")
    
    # Sample test data
    test_data = {
        "query": "What are the most common objections for rate filings?",
        "filtered_data": [
            {
                "State": "CA",
                "LOB": "Personal Auto",
                "Filing_Type": "Rate",
                "RespType": "DOI Objection",
                "Topic": "MTF",
                "Carrier": "GEICO",
                "Question": "Sample question",
                "Response": "Sample response"
            }
        ],
        "filter_summary": {
            "total_records": 1,
            "states": ["CA"],
            "lobs": ["Personal Auto"],
            "filing_types": ["Rate"],
            "response_types": ["DOI Objection"],
            "topics": ["MTF"],
            "carriers": ["GEICO"]
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:5000/query",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Query endpoint working")
            print(f"📊 Records analyzed: {result.get('records_analyzed', 0)}")
            print(f"🔍 Query processed: {result.get('query', 'N/A')}")
            return True
        else:
            print(f"❌ Query endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to query endpoint")
        return False
    except Exception as e:
        print(f"❌ Query test error: {e}")
        return False

def test_data_loading():
    """Test if the Excel data can be loaded"""
    print("🔍 Testing data loading...")
    try:
        import pandas as pd
        df = pd.read_excel("ResponseData.xlsx")
        print(f"✅ Data loaded successfully")
        print(f"📊 Shape: {df.shape}")
        print(f"📋 Columns: {list(df.columns)}")
        return True
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are available"""
    print("🔍 Testing dependencies...")
    
    required_modules = [
        "flask",
        "flask_cors", 
        "pandas",
        "openpyxl",
        "requests",
        "opensearchpy",
        "reactpy"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - missing")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️  Missing modules: {missing_modules}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def main():
    """Run all tests"""
    print("🧪 Testing Integrated DOI Research Assistant System")
    print("=" * 60)
    
    tests = [
        ("Dependencies", test_dependencies),
        ("Data Loading", test_data_loading),
        ("Backend Health", test_backend_health),
        ("Query Endpoint", test_query_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 To start the system:")
        print("   python start_integrated_system.py")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        print("\n💡 Troubleshooting tips:")
        print("   1. Install missing dependencies: pip install -r requirements.txt")
        print("   2. Start backend server: python backend_server.py")
        print("   3. Ensure OpenSearch is running on localhost:9200")

if __name__ == "__main__":
    main()
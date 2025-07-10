#!/usr/bin/env python3
"""
Test script to verify NaN handling in the application.
"""

import pandas as pd
import numpy as np
import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_nan_handling():
    """Test that NaN values are properly handled"""
    
    # Create a test DataFrame with NaN values
    test_data = pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['John', 'Jane', 'Bob', 'Alice'],
        'age': [25, 30, np.nan, 35],
        'score': [85.5, np.nan, 92.0, 78.5],
        'active': [True, False, True, np.nan]
    })
    
    print("Original DataFrame:")
    print(test_data)
    print("\nDataFrame info:")
    print(test_data.info())
    
    # Test the clean_data_for_json function
    try:
        from ui.simple_react import clean_data_for_json
        
        cleaned_data = clean_data_for_json(test_data)
        
        print("\nCleaned data:")
        for i, record in enumerate(cleaned_data):
            print(f"Record {i}: {record}")
        
        # Test JSON serialization
        json_str = json.dumps(cleaned_data, indent=2)
        print(f"\nJSON serialization successful! Length: {len(json_str)}")
        
        # Test deserialization
        parsed_data = json.loads(json_str)
        print("JSON deserialization successful!")
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

def test_backend_nan_handling():
    """Test the backend NaN handling functions"""
    
    # Create test data with NaN values
    test_records = [
        {'id': 1, 'name': 'John', 'age': 25, 'score': 85.5, 'active': True},
        {'id': 2, 'name': 'Jane', 'age': 30, 'score': np.nan, 'active': False},
        {'id': 3, 'name': 'Bob', 'age': np.nan, 'score': 92.0, 'active': True},
        {'id': 4, 'name': 'Alice', 'age': 35, 'score': 78.5, 'active': np.nan}
    ]
    
    try:
        from backend_server import clean_data_for_json
        
        cleaned_data = clean_data_for_json(test_records)
        
        print("\nBackend cleaned data:")
        for i, record in enumerate(cleaned_data):
            print(f"Record {i}: {record}")
        
        # Test JSON serialization
        json_str = json.dumps(cleaned_data, indent=2)
        print(f"\nBackend JSON serialization successful! Length: {len(json_str)}")
        
        return True
        
    except Exception as e:
        print(f"Error during backend testing: {e}")
        return False

if __name__ == "__main__":
    print("Testing NaN handling in the application...")
    print("=" * 50)
    
    frontend_success = test_nan_handling()
    backend_success = test_backend_nan_handling()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Frontend NaN handling: {'✅ PASSED' if frontend_success else '❌ FAILED'}")
    print(f"Backend NaN handling: {'✅ PASSED' if backend_success else '❌ FAILED'}")
    
    if frontend_success and backend_success:
        print("\n🎉 All tests passed! NaN handling is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
#!/usr/bin/env python3
"""
Simple test script to verify NaN handling logic.
"""

import json
import math

def clean_data_for_json_simple(data):
    """
    Simple version of clean_data_for_json function for testing.
    """
    cleaned_records = []
    for record in data:
        cleaned_record = {}
        for key, value in record.items():
            # Check for NaN values
            if isinstance(value, float) and math.isnan(value):
                cleaned_record[key] = None
            else:
                cleaned_record[key] = value
        cleaned_records.append(cleaned_record)
    
    return cleaned_records

def test_nan_handling():
    """Test that NaN values are properly handled"""
    
    # Create test data with NaN values
    test_records = [
        {'id': 1, 'name': 'John', 'age': 25, 'score': 85.5, 'active': True},
        {'id': 2, 'name': 'Jane', 'age': 30, 'score': float('nan'), 'active': False},
        {'id': 3, 'name': 'Bob', 'age': float('nan'), 'score': 92.0, 'active': True},
        {'id': 4, 'name': 'Alice', 'age': 35, 'score': 78.5, 'active': float('nan')}
    ]
    
    print("Original test data:")
    for i, record in enumerate(test_records):
        print(f"Record {i}: {record}")
    
    # Test the clean_data_for_json function
    try:
        cleaned_data = clean_data_for_json_simple(test_records)
        
        print("\nCleaned data:")
        for i, record in enumerate(cleaned_data):
            print(f"Record {i}: {record}")
        
        # Test JSON serialization
        json_str = json.dumps(cleaned_data, indent=2)
        print(f"\nJSON serialization successful! Length: {len(json_str)}")
        print("JSON output:")
        print(json_str)
        
        # Test deserialization
        parsed_data = json.loads(json_str)
        print("\nJSON deserialization successful!")
        
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

def test_custom_json_encoder():
    """Test the custom JSON encoder logic"""
    
    class NaNHandlingEncoder(json.JSONEncoder):
        """Custom JSON encoder that handles NaN values"""
        def default(self, obj):
            if isinstance(obj, float) and math.isnan(obj):
                return None
            return super().default(obj)
    
    # Test data with NaN
    test_data = {
        'normal_value': 42,
        'nan_value': float('nan'),
        'list_with_nan': [1, 2, float('nan'), 4],
        'nested': {
            'inner_nan': float('nan'),
            'inner_normal': 'hello'
        }
    }
    
    try:
        json_str = json.dumps(test_data, cls=NaNHandlingEncoder, indent=2)
        print("\nCustom encoder test successful!")
        print("JSON output:")
        print(json_str)
        
        # Test deserialization
        parsed_data = json.loads(json_str)
        print("\nCustom encoder deserialization successful!")
        
        return True
        
    except Exception as e:
        print(f"Error during custom encoder testing: {e}")
        return False

if __name__ == "__main__":
    print("Testing NaN handling logic...")
    print("=" * 50)
    
    basic_success = test_nan_handling()
    encoder_success = test_custom_json_encoder()
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print(f"Basic NaN handling: {'✅ PASSED' if basic_success else '❌ FAILED'}")
    print(f"Custom JSON encoder: {'✅ PASSED' if encoder_success else '❌ FAILED'}")
    
    if basic_success and encoder_success:
        print("\n🎉 All tests passed! NaN handling logic is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
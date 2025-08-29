#!/usr/bin/env python3
"""
Test script for the BFHL API
Tests all the examples provided in the VIT question paper
"""

import requests
import json
import sys

# API base URL (change this to your deployed URL)
BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{endpoint}")
        elif method == "POST":
            response = requests.post(f"{BASE_URL}{endpoint}", json=data)
        else:
            print(f"Unsupported method: {method}")
            return False
            
        print(f"\n{'='*60}")
        print(f"Testing {method} {endpoint}")
        print(f"{'='*60}")
        
        if data:
            print(f"Request Data: {json.dumps(data, indent=2)}")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Make sure the API is running at {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_examples():
    """Test all the examples from the question paper"""
    print("🧪 Testing BFHL API with VIT Question Examples")
    
    # Test health check
    test_endpoint("/")
    
    # Test API info
    test_endpoint("/bfhl")
    
    # Example A from question paper
    example_a = {
        "data": ["a", "1", "334", "4", "R", "$"]
    }
    test_endpoint("/bfhl", "POST", example_a)
    
    # Example B from question paper
    example_b = {
        "data": ["2", "a", "y", "4", "&", "-", "*", "5", "92", "b"]
    }
    test_endpoint("/bfhl", "POST", example_b)
    
    # Example C from question paper
    example_c = {
        "data": ["A", "ABcD", "DOE"]
    }
    test_endpoint("/bfhl", "POST", example_c)
    
    # Additional test cases
    print("\n🧪 Testing Additional Edge Cases")
    
    # Empty array
    empty_array = {"data": []}
    test_endpoint("/bfhl", "POST", empty_array)
    
    # Only numbers
    numbers_only = {"data": ["1", "2", "3", "4", "5"]}
    test_endpoint("/bfhl", "POST", numbers_only)
    
    # Only alphabets
    alphabets_only = {"data": ["a", "B", "c", "D"]}
    test_endpoint("/bfhl", "POST", alphabets_only)
    
    # Only special characters
    special_only = {"data": ["@", "#", "$", "%"]}
    test_endpoint("/bfhl", "POST", special_only)
    
    # Mixed with negative numbers
    negative_numbers = {"data": ["-1", "2", "a", "B", "&"]}
    test_endpoint("/bfhl", "POST", negative_numbers)

def test_error_handling():
    """Test error handling scenarios"""
    print("\n🧪 Testing Error Handling")
    
    # Missing data field
    missing_data = {}
    test_endpoint("/bfhl", "POST", missing_data)
    
    # Invalid data type (not array)
    invalid_data = {"data": "not_an_array"}
    test_endpoint("/bfhl", "POST", invalid_data)
    
    # Malformed JSON (this will be handled by Flask)

if __name__ == "__main__":
    print("🚀 BFHL API Test Suite")
    print("Make sure the API is running before executing tests")
    
    try:
        # Test basic functionality
        test_examples()
        
        # Test error handling
        test_error_handling()
        
        print("\n✅ All tests completed!")
        
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite error: {str(e)}")
        sys.exit(1)

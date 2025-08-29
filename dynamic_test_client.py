#!/usr/bin/env python3
"""
Dynamic Test Client for BFHL API
Generates different types of test data and tests the API dynamically
"""

import requests
import json
import random
import string
import time
from typing import List, Dict, Any

class DynamicTestClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def generate_random_data(self, count: int = 10, data_types: List[str] = None) -> List[str]:
        """Generate random test data"""
        if data_types is None:
            data_types = ['number', 'alphabet', 'special']
            
        data = []
        for _ in range(count):
            data_type = random.choice(data_types)
            
            if data_type == 'number':
                # Generate random numbers (positive, negative, zero)
                num = random.randint(-100, 100)
                data.append(str(num))
                
            elif data_type == 'alphabet':
                # Generate random alphabets (single char or words)
                length = random.randint(1, 8)
                word = ''.join(random.choices(string.ascii_letters, k=length))
                data.append(word)
                
            elif data_type == 'special':
                # Generate random special characters
                special_chars = ['@', '#', '$', '%', '&', '*', '-', '+', '=', '!', '?', '^', '~', '(', ')', '[', ']', '{', '}']
                data.append(random.choice(special_chars))
                
        return data
    
    def generate_pattern_data(self, pattern: str, count: int = 10) -> List[str]:
        """Generate data based on specific patterns"""
        data = []
        
        if pattern == 'fibonacci':
            # Generate Fibonacci sequence
            a, b = 0, 1
            for _ in range(count):
                data.append(str(a))
                a, b = b, a + b
                
        elif pattern == 'prime':
            # Generate prime numbers
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
            data = [str(p) for p in primes[:count]]
            
        elif pattern == 'vowels':
            # Generate vowels with consonants
            vowels = 'aeiou'
            consonants = 'bcdfghjklmnpqrstvwxyz'
            for i in range(count):
                if i % 2 == 0:
                    data.append(random.choice(vowels))
                else:
                    data.append(random.choice(consonants))
                    
        elif pattern == 'binary':
            # Generate binary-like pattern
            for i in range(count):
                if i % 2 == 0:
                    data.append('0')
                else:
                    data.append('1')
                    
        elif pattern == 'alternating':
            # Generate alternating pattern
            for i in range(count):
                if i % 3 == 0:
                    data.append(str(i))
                elif i % 3 == 1:
                    data.append(chr(97 + (i % 26)))  # a-z
                else:
                    data.append(['@', '#', '$', '%', '&'][i % 5])
                    
        return data
    
    def generate_edge_case_data(self, case: str) -> List[str]:
        """Generate edge case data"""
        if case == 'empty':
            return []
            
        elif case == 'single':
            return ['a']
            
        elif case == 'large_numbers':
            return [str(random.randint(1000000, 9999999)) for _ in range(5)]
            
        elif case == 'very_long_strings':
            return [''.join(random.choices(string.ascii_letters, k=50)) for _ in range(3)]
            
        elif case == 'mixed_case':
            return ['a', 'B', 'c', 'D', 'e', 'F']
            
        elif case == 'unicode':
            return ['ñ', 'é', 'ü', 'ß', 'å', 'ø']
            
        elif case == 'spaces':
            return [' ', '  ', '   ', '    ', '     ']
            
        elif case == 'newlines':
            return ['\n', '\r', '\t', '\f', '\v']
            
        return []
    
    def test_api_with_data(self, data: List[str], description: str = "") -> Dict[str, Any]:
        """Test the API with given data"""
        try:
            payload = {"data": data}
            
            print(f"\n🧪 Testing: {description}")
            print(f"📊 Data: {data[:10]}{'...' if len(data) > 10 else ''}")
            print(f"📏 Length: {len(data)}")
            
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/bfhl", json=payload)
            end_time = time.time()
            
            result = {
                "description": description,
                "data_length": len(data),
                "status_code": response.status_code,
                "response_time": round(end_time - start_time, 3),
                "success": response.status_code == 200
            }
            
            if response.status_code == 200:
                response_data = response.json()
                result.update({
                    "even_count": len(response_data.get("even_numbers", [])),
                    "odd_count": len(response_data.get("odd_numbers", [])),
                    "alphabet_count": len(response_data.get("alphabets", [])),
                    "special_count": len(response_data.get("special_characters", [])),
                    "sum": response_data.get("sum", "0"),
                    "concat_length": len(response_data.get("concat_string", ""))
                })
                print(f"✅ Success - Response time: {result['response_time']}s")
            else:
                print(f"❌ Failed - Status: {response.status_code}")
                
            return result
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "description": description,
                "error": str(e),
                "success": False
            }
    
    def run_comprehensive_tests(self):
        """Run comprehensive tests with different data patterns"""
        print("🚀 Dynamic BFHL API Test Suite")
        print("=" * 60)
        
        test_results = []
        
        # Test 1: Random data with different sizes
        print("\n📊 Testing Random Data Generation")
        for size in [5, 10, 20, 30]:
            data = self.generate_random_data(size)
            result = self.test_api_with_data(data, f"Random data (size: {size})")
            test_results.append(result)
        
        # Test 2: Pattern-based data
        print("\n🔄 Testing Pattern-Based Data")
        patterns = ['fibonacci', 'prime', 'vowels', 'binary', 'alternating']
        for pattern in patterns:
            data = self.generate_pattern_data(pattern, 15)
            result = self.test_api_with_data(data, f"Pattern: {pattern}")
            test_results.append(result)
        
        # Test 3: Edge cases
        print("\n⚠️  Testing Edge Cases")
        edge_cases = ['empty', 'single', 'large_numbers', 'very_long_strings', 'mixed_case']
        for case in edge_cases:
            data = self.generate_edge_case_data(case)
            result = self.test_api_with_data(data, f"Edge case: {case}")
            test_results.append(result)
        
        # Test 4: Specific data type combinations
        print("\n🎯 Testing Specific Data Type Combinations")
        
        # Only numbers
        numbers_only = self.generate_random_data(20, ['number'])
        result = self.test_api_with_data(numbers_only, "Only numbers")
        test_results.append(result)
        
        # Only alphabets
        alphabets_only = self.generate_random_data(20, ['alphabet'])
        result = self.test_api_with_data(alphabets_only, "Only alphabets")
        test_results.append(result)
        
        # Only special characters
        special_only = self.generate_random_data(20, ['special'])
        result = self.test_api_with_data(special_only, "Only special characters")
        test_results.append(result)
        
        # Test 5: Stress test with large data
        print("\n💪 Stress Testing")
        large_data = self.generate_random_data(50)
        result = self.test_api_with_data(large_data, "Large dataset (50 items)")
        test_results.append(result)
        
        # Generate summary report
        self.generate_summary_report(test_results)
        
        return test_results
    
    def generate_summary_report(self, results: List[Dict[str, Any]]):
        """Generate a summary report of all tests"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY REPORT")
        print("=" * 60)
        
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get('success', False))
        failed_tests = total_tests - successful_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Successful: {successful_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(successful_tests/total_tests)*100:.1f}%")
        
        if successful_tests > 0:
            avg_response_time = sum(r.get('response_time', 0) for r in results if r.get('success', False)) / successful_tests
            print(f"Average Response Time: {avg_response_time:.3f}s")
        
        # Show failed tests
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in results:
                if not result.get('success', False):
                    print(f"  - {result.get('description', 'Unknown')}: {result.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 60)

def main():
    """Main function to run the dynamic test client"""
    client = DynamicTestClient()
    
    try:
        # Check if API is running
        response = client.session.get(f"{client.base_url}/")
        if response.status_code != 200:
            print(f"❌ API is not running at {client.base_url}")
            print("Please start the API server first")
            return
        
        print("✅ API is running successfully!")
        
        # Run comprehensive tests
        results = client.run_comprehensive_tests()
        
        print("\n🎉 Dynamic testing completed!")
        print(f"📝 Results saved for {len(results)} test cases")
        
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    main()

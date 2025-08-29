#!/usr/bin/env python3
"""
Configuration-Based Test Runner for BFHL API
Uses test_config.json to run predefined test scenarios
"""

import requests
import json
import time
from typing import Dict, List, Any
from pathlib import Path

class ConfigTestRunner:
    def __init__(self, base_url: str = "http://localhost:8000", config_file: str = "test_config.json"):
        self.base_url = base_url
        self.config_file = config_file
        self.session = requests.Session()
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load test configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file {self.config_file} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing configuration file: {e}")
            return {}
    
    def validate_response(self, response_data: Dict[str, Any], expected: Dict[str, Any], test_name: str) -> Dict[str, Any]:
        """Validate API response against expected results"""
        validation_result = {
            "test_name": test_name,
            "passed": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        required_fields = self.config.get("validation_rules", {}).get("required_fields", [])
        for field in required_fields:
            if field not in response_data:
                validation_result["errors"].append(f"Missing required field: {field}")
                validation_result["passed"] = False
        
        # Check expected values
        for key, expected_value in expected.items():
            if key in response_data:
                actual_value = response_data[key]
                if actual_value != expected_value:
                    validation_result["errors"].append(
                        f"Field '{key}': expected {expected_value}, got {actual_value}"
                    )
                    validation_result["passed"] = False
            else:
                validation_result["warnings"].append(f"Expected field '{key}' not found in response")
        
        # Check data type consistency
        if "sum" in response_data:
            try:
                int(response_data["sum"])
            except ValueError:
                validation_result["errors"].append("Sum field is not a valid number string")
                validation_result["passed"] = False
        
        # Check array consistency
        array_fields = ["odd_numbers", "even_numbers", "alphabets", "special_characters"]
        for field in array_fields:
            if field in response_data and not isinstance(response_data[field], list):
                validation_result["errors"].append(f"Field '{field}' is not an array")
                validation_result["passed"] = False
        
        return validation_result
    
    def run_test_scenario(self, scenario_name: str, scenario_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Run all tests in a specific scenario"""
        print(f"\n🔍 Running Scenario: {scenario_name}")
        print(f"📝 Description: {scenario_data.get('description', 'No description')}")
        print("-" * 60)
        
        results = []
        tests = scenario_data.get('tests', [])
        
        for test in tests:
            test_name = test.get('name', 'Unnamed Test')
            test_data = test.get('data', [])
            expected = test.get('expected', {})
            
            print(f"\n🧪 Test: {test_name}")
            print(f"📊 Input: {test_data[:10]}{'...' if len(test_data) > 10 else ''}")
            
            # Run the test
            test_result = self.run_single_test(test_data, expected, test_name)
            results.append(test_result)
            
            # Display result
            if test_result["passed"]:
                print(f"✅ PASSED - Response time: {test_result.get('response_time', 0):.3f}s")
            else:
                print(f"❌ FAILED")
                for error in test_result.get("errors", []):
                    print(f"   🚨 {error}")
                for warning in test_result.get("warnings", []):
                    print(f"   ⚠️  {warning}")
        
        return results
    
    def run_single_test(self, test_data: List[str], expected: Dict[str, Any], test_name: str) -> Dict[str, Any]:
        """Run a single test case"""
        try:
            payload = {"data": test_data}
            
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/bfhl", json=payload)
            end_time = time.time()
            
            result = {
                "test_name": test_name,
                "data_length": len(test_data),
                "status_code": response.status_code,
                "response_time": round(end_time - start_time, 3),
                "passed": False,
                "errors": [],
                "warnings": []
            }
            
            if response.status_code == 200:
                response_data = response.json()
                
                # Validate response
                validation = self.validate_response(response_data, expected, test_name)
                result.update(validation)
                
                # Add response summary
                result["response_summary"] = {
                    "even_count": len(response_data.get("even_numbers", [])),
                    "odd_count": len(response_data.get("odd_numbers", [])),
                    "alphabet_count": len(response_data.get("alphabets", [])),
                    "special_count": len(response_data.get("special_characters", [])),
                    "sum": response_data.get("sum", "0"),
                    "concat_length": len(response_data.get("concat_string", ""))
                }
            else:
                result["errors"].append(f"API returned status code {response.status_code}")
                try:
                    error_data = response.json()
                    result["errors"].append(f"Error message: {error_data.get('error', 'Unknown error')}")
                except:
                    result["errors"].append("Could not parse error response")
            
            return result
            
        except Exception as e:
            return {
                "test_name": test_name,
                "error": str(e),
                "passed": False,
                "errors": [f"Test execution error: {str(e)}"]
            }
    
    def run_all_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """Run all test scenarios"""
        print("🚀 Configuration-Based BFHL API Test Suite")
        print("=" * 60)
        
        if not self.config:
            print("❌ No configuration loaded. Exiting.")
            return {}
        
        all_results = {}
        scenarios = self.config.get("test_scenarios", {})
        
        for scenario_name, scenario_data in scenarios.items():
            results = self.run_test_scenario(scenario_name, scenario_data)
            all_results[scenario_name] = results
        
        return all_results
    
    def generate_report(self, all_results: Dict[str, List[Dict[str, Any]]]):
        """Generate comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST REPORT")
        print("=" * 60)
        
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_response_time = 0
        valid_tests = 0
        
        for scenario_name, results in all_results.items():
            print(f"\n📋 Scenario: {scenario_name}")
            print(f"   Tests: {len(results)}")
            
            scenario_passed = sum(1 for r in results if r.get('passed', False))
            scenario_failed = len(results) - scenario_passed
            
            print(f"   ✅ Passed: {scenario_passed}")
            print(f"   ❌ Failed: {scenario_failed}")
            
            total_tests += len(results)
            total_passed += scenario_passed
            total_failed += scenario_failed
            
            # Calculate response times
            for result in results:
                if result.get('response_time'):
                    total_response_time += result['response_time']
                    valid_tests += 1
        
        # Overall statistics
        print(f"\n📈 OVERALL STATISTICS")
        print(f"   Total Tests: {total_tests}")
        print(f"   Total Passed: {total_passed} ✅")
        print(f"   Total Failed: {total_failed} ❌")
        print(f"   Success Rate: {(total_passed/total_tests)*100:.1f}%" if total_tests > 0 else "   Success Rate: N/A")
        
        if valid_tests > 0:
            avg_response_time = total_response_time / valid_tests
            print(f"   Average Response Time: {avg_response_time:.3f}s")
        
        # Failed tests summary
        if total_failed > 0:
            print(f"\n❌ FAILED TESTS SUMMARY:")
            for scenario_name, results in all_results.items():
                for result in results:
                    if not result.get('passed', False):
                        print(f"   - {scenario_name}: {result.get('test_name', 'Unknown')}")
                        for error in result.get('errors', [])[:2]:  # Show first 2 errors
                            print(f"     🚨 {error}")
        
        print("\n" + "=" * 60)
        
        return {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": (total_passed/total_tests)*100 if total_tests > 0 else 0,
            "avg_response_time": total_response_time / valid_tests if valid_tests > 0 else 0
        }

def main():
    """Main function to run the configuration-based test suite"""
    runner = ConfigTestRunner()
    
    try:
        # Check if API is running
        response = runner.session.get(f"{runner.base_url}/")
        if response.status_code != 200:
            print(f"❌ API is not running at {runner.base_url}")
            print("Please start the API server first")
            return
        
        print("✅ API is running successfully!")
        
        # Run all test scenarios
        all_results = runner.run_all_scenarios()
        
        if all_results:
            # Generate comprehensive report
            summary = runner.generate_report(all_results)
            
            print(f"\n🎉 Configuration-based testing completed!")
            print(f"📝 Summary: {summary['total_passed']}/{summary['total_tests']} tests passed")
            
            # Save results to file
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results_file = f"test_results_{timestamp}.json"
            
            with open(results_file, 'w') as f:
                json.dump({
                    "timestamp": timestamp,
                    "summary": summary,
                    "detailed_results": all_results
                }, f, indent=2)
            
            print(f"💾 Detailed results saved to: {results_file}")
        
    except KeyboardInterrupt:
        print("\n⏹️  Testing interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")

if __name__ == "__main__":
    main()

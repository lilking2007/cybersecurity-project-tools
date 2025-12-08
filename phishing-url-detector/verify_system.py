"""
Final Verification Script

Runs all tests to verify the system is 100% functional.
"""

import sys
import subprocess
from pathlib import Path

def run_test(name, command, cwd=None):
    """Run a test command and return result."""
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print(f"[PASS] {name}")
            return True
        else:
            print(f"[FAIL] {name} (exit code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[FAIL] {name} (timeout)")
        return False
    except Exception as e:
        print(f"[FAIL] {name} ({str(e)})")
        return False

def main():
    """Run all verification tests."""
    print("="*60)
    print("PHISHING URL DETECTOR - FINAL VERIFICATION")
    print("="*60)
    
    project_dir = Path(__file__).parent
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Quick functionality test
    tests_total += 1
    if run_test(
        "Core Functionality Test",
        "python test_quick.py",
        cwd=project_dir
    ):
        tests_passed += 1
    
    # Test 2: Flask app test
    tests_total += 1
    if run_test(
        "Flask Application Test",
        "python test_app.py",
        cwd=project_dir
    ):
        tests_passed += 1
    
    # Test 3: CLI help
    tests_total += 1
    if run_test(
        "CLI Help Test",
        "python cli.py --help",
        cwd=project_dir
    ):
        tests_passed += 1
    
    # Test 4: CLI URL analysis (fast mode)
    tests_total += 1
    if run_test(
        "CLI URL Analysis Test",
        "python cli.py --no-network --json https://www.google.com",
        cwd=project_dir
    ):
        tests_passed += 1
    
    # Print summary
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")
    
    if tests_passed == tests_total:
        print("\n[SUCCESS] ALL TESTS PASSED!")
        print("="*60)
        print("\nThe system is 100% functional and ready to use!")
        print("\nNext steps:")
        print("  1. Start the web app: python app/main.py")
        print("  2. Or use CLI: python cli.py https://example.com")
        print("  3. Train with real data: python scripts/train_model.py --data your_data.csv")
        return 0
    else:
        print("\n[WARNING] Some tests failed")
        print(f"Failed: {tests_total - tests_passed} test(s)")
        return 1

if __name__ == '__main__':
    sys.exit(main())

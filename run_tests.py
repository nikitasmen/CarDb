#!/usr/bin/env python3
"""
Test runner script for CarDb Mobile App
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def run_command(command, description):
    """Run a command and return the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print(f"Return code: {e.returncode}")
        if e.stdout:
            print("STDOUT:")
            print(e.stdout)
        if e.stderr:
            print("STDERR:")
            print(e.stderr)
        return False

def run_tests(test_type="all", verbose=False, coverage=False, parallel=False):
    """Run tests based on the specified type"""
    
    # Base pytest command
    base_cmd = "python -m pytest"
    
    if verbose:
        base_cmd += " -v"
    
    if coverage:
        base_cmd += " --cov=app --cov=interfaces --cov-report=html --cov-report=term"
    
    if parallel:
        base_cmd += " -n auto"  # Requires pytest-xdist
    
    # Test directory
    test_dir = "tests/"
    
    # Test type specific commands
    if test_type == "unit":
        cmd = f"{base_cmd} {test_dir}unit/ -m unit"
        description = "Unit Tests"
    elif test_type == "integration":
        cmd = f"{base_cmd} {test_dir}integration/ -m integration"
        description = "Integration Tests"
    elif test_type == "ui":
        cmd = f"{base_cmd} {test_dir}ui/ -m ui"
        description = "UI Tests"
    elif test_type == "performance":
        cmd = f"{base_cmd} {test_dir}performance/ -m performance"
        description = "Performance Tests"
    elif test_type == "mobile":
        cmd = f"{base_cmd} {test_dir} -m mobile"
        description = "Mobile-Specific Tests"
    elif test_type == "fast":
        cmd = f"{base_cmd} {test_dir} -m 'not slow'"
        description = "Fast Tests (excluding slow tests)"
    elif test_type == "all":
        cmd = f"{base_cmd} {test_dir}"
        description = "All Tests"
    else:
        print(f"❌ Unknown test type: {test_type}")
        return False
    
    return run_command(cmd, description)

def run_linting():
    """Run code linting"""
    commands = [
        ("python -m flake8 app/ interfaces/ --max-line-length=100 --ignore=E203,W503", "Code Linting (flake8)"),
        ("python -m flake8 tests/ --max-line-length=100 --ignore=E203,W503", "Test Code Linting (flake8)"),
    ]
    
    success = True
    for cmd, description in commands:
        if not run_command(cmd, description):
            success = False
    
    return success

def run_type_checking():
    """Run type checking"""
    try:
        import mypy
        cmd = "python -m mypy app/ interfaces/ --ignore-missing-imports"
        return run_command(cmd, "Type Checking (mypy)")
    except ImportError:
        print("⚠️  mypy not installed, skipping type checking")
        return True

def run_security_check():
    """Run security checks"""
    try:
        import bandit
        cmd = "python -m bandit -r app/ interfaces/ -f json -o security_report.json"
        return run_command(cmd, "Security Check (bandit)")
    except ImportError:
        print("⚠️  bandit not installed, skipping security check")
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="CarDb Mobile App Test Runner")
    parser.add_argument(
        "--type", 
        choices=["all", "unit", "integration", "ui", "performance", "mobile", "fast"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--coverage", "-c",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--parallel", "-p",
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--lint",
        action="store_true",
        help="Run linting checks"
    )
    parser.add_argument(
        "--type-check",
        action="store_true",
        help="Run type checking"
    )
    parser.add_argument(
        "--security",
        action="store_true",
        help="Run security checks"
    )
    parser.add_argument(
        "--all-checks",
        action="store_true",
        help="Run all checks (tests, linting, type checking, security)"
    )
    
    args = parser.parse_args()
    
    print("🚗 CarDb Mobile App Test Runner")
    print("=" * 50)
    
    success = True
    
    # Run tests
    if args.all_checks or not any([args.lint, args.type_check, args.security]):
        if not run_tests(args.type, args.verbose, args.coverage, args.parallel):
            success = False
    
    # Run additional checks if requested
    if args.all_checks or args.lint:
        if not run_linting():
            success = False
    
    if args.all_checks or args.type_check:
        if not run_type_checking():
            success = False
    
    if args.all_checks or args.security:
        if not run_security_check():
            success = False
    
    # Print summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All checks passed!")
        sys.exit(0)
    else:
        print("❌ Some checks failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()


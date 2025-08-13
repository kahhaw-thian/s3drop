#!/usr/bin/env python3
"""
Test script to demonstrate S3Drop auto-creation feature.
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path

def test_auto_creation():
    """Test S3Drop auto-creation functionality."""
    
    # Create a test file
    test_file = "s3drop_test.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file for S3Drop auto-creation feature.")
    
    # Use a unique drop zone name
    import time
    drop_zone = f"s3drop-test-{int(time.time())}"
    
    print("🧪 Testing S3Drop Auto-Creation")
    print("=" * 50)
    print(f"📁 Test file: {test_file}")
    print(f"🪣 Drop zone: {drop_zone}")
    print()
    
    try:
        # Test auto-creation by trying to drop a file
        print("🚀 Testing auto-creation...")
        result = subprocess.run([
            'python3', 's3drop.py', drop_zone, 'drop', test_file, '--share'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Auto-creation test PASSED!")
            print("\nOutput:")
            print(result.stdout)
            
            # Clean up - delete the test file from S3
            print("\n🧹 Cleaning up...")
            cleanup_result = subprocess.run([
                'aws', 's3', 'rm', f's3://{drop_zone}/{test_file}'
            ], capture_output=True, text=True)
            
            if cleanup_result.returncode == 0:
                print("✅ Test file removed from S3")
            
            # Note: We don't delete the bucket as it might be useful for further testing
            print(f"💡 Drop zone '{drop_zone}' left for your use")
            
        else:
            print("❌ Auto-creation test FAILED!")
            print("\nError output:")
            print(result.stderr)
            
            if "Permission denied" in result.stderr:
                print("\n💡 This is likely due to insufficient AWS permissions.")
                print("💡 Required permissions: s3:CreateBucket, s3:PutBucketPublicAccessBlock")
            elif "already taken" in result.stderr:
                print("\n💡 The bucket name is already taken globally.")
                print("💡 This is normal - S3 bucket names must be globally unique.")
    
    except subprocess.TimeoutExpired:
        print("❌ Test timed out after 60 seconds")
    except FileNotFoundError:
        print("❌ s3drop.py not found. Make sure you're in the correct directory.")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
    
    finally:
        # Clean up local test file
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"🧹 Removed local test file: {test_file}")

def test_no_auto_create():
    """Test the --no-auto-create flag."""
    
    print("\n🧪 Testing --no-auto-create Flag")
    print("=" * 50)
    
    # Use a non-existent drop zone
    import time
    drop_zone = f"s3drop-noauto-{int(time.time())}"
    
    try:
        result = subprocess.run([
            'python3', 's3drop.py', drop_zone, 'list', '--no-auto-create'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0 and "does not exist" in result.stderr:
            print("✅ --no-auto-create flag works correctly!")
            print("✅ S3Drop correctly refused to create the drop zone")
        else:
            print("❌ --no-auto-create flag test failed")
            print(f"Return code: {result.returncode}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
    
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    print("S3Drop Auto-Creation Test Suite")
    print("This will test S3Drop's ability to automatically create drop zones.")
    print()
    
    # Check if AWS credentials are configured
    try:
        result = subprocess.run(['aws', 'sts', 'get-caller-identity'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ AWS credentials are configured")
        else:
            print("❌ AWS credentials not configured. Run: aws configure")
            sys.exit(1)
    except Exception:
        print("❌ AWS CLI not found or not configured")
        sys.exit(1)
    
    # Run tests
    test_auto_creation()
    test_no_auto_create()
    
    print("\n🎉 Test suite completed!")
    print("💡 If auto-creation failed due to permissions, that's normal.")
    print("💡 The feature will work when you have proper AWS permissions.")
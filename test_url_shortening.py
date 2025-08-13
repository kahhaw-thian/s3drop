#!/usr/bin/env python3
"""
Test script for S3Drop URL shortening functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from s3drop import S3Drop

def test_url_shortening_services():
    """Test all URL shortening services."""
    
    # Test URL (a long AWS S3 presigned URL example)
    test_url = ("https://example-bucket.s3.amazonaws.com/test-file.pdf?"
                "X-Amz-Algorithm=AWS4-HMAC-SHA256&"
                "X-Amz-Credential=AKIAIOSFODNN7EXAMPLE%2F20240115%2Fus-east-1%2Fs3%2Faws4_request&"
                "X-Amz-Date=20240115T120000Z&"
                "X-Amz-Expires=86400&"
                "X-Amz-SignedHeaders=host&"
                "X-Amz-Signature=abcd1234567890abcdef1234567890abcdef1234567890abcdef1234567890ab")
    
    print("🧪 Testing S3Drop URL Shortening Services")
    print("=" * 60)
    print(f"📏 Original URL length: {len(test_url)} characters")
    print(f"🔗 Test URL: {test_url[:80]}...")
    print()
    
    # Create a dummy S3Drop instance (we won't use S3 features)
    s3drop = S3Drop.__new__(S3Drop)  # Create without calling __init__
    
    services = ['tinyurl', 'isgd', 'vgd', '1ptco']
    results = {}
    
    for service in services:
        print(f"🔧 Testing {service.upper()}...")
        try:
            short_url = s3drop.shorten_url(test_url, service)
            if short_url != test_url:
                results[service] = {
                    'success': True,
                    'url': short_url,
                    'length': len(short_url),
                    'saved': len(test_url) - len(short_url)
                }
                print(f"✅ Success: {short_url}")
                print(f"📏 Length: {len(short_url)} characters")
                print(f"💾 Saved: {len(test_url) - len(short_url)} characters")
            else:
                results[service] = {'success': False, 'error': 'Service returned original URL'}
                print(f"❌ Failed: Service returned original URL")
        except Exception as e:
            results[service] = {'success': False, 'error': str(e)}
            print(f"❌ Failed: {e}")
        print()
    
    # Summary
    print("📊 Summary:")
    print("-" * 40)
    successful_services = [s for s, r in results.items() if r['success']]
    failed_services = [s for s, r in results.items() if not r['success']]
    
    if successful_services:
        print(f"✅ Working services: {', '.join(successful_services)}")
        
        # Find the shortest URL
        shortest = min(successful_services, 
                      key=lambda s: results[s]['length'])
        print(f"🏆 Shortest URL: {shortest.upper()} ({results[shortest]['length']} chars)")
        
        # Find most characters saved
        best_savings = max(successful_services,
                          key=lambda s: results[s]['saved'])
        print(f"💾 Best savings: {best_savings.upper()} ({results[best_savings]['saved']} chars saved)")
    
    if failed_services:
        print(f"❌ Failed services: {', '.join(failed_services)}")
        for service in failed_services:
            print(f"   {service}: {results[service]['error']}")
    
    print(f"\n🎯 Recommendation: Use {'tinyurl' if 'tinyurl' in successful_services else successful_services[0] if successful_services else 'none'}")
    
    return results

def test_service_availability():
    """Test if URL shortening services are available."""
    print("\n🌐 Testing Service Availability")
    print("=" * 40)
    
    import requests
    
    services = {
        'tinyurl': 'http://tinyurl.com',
        'isgd': 'https://is.gd',
        'vgd': 'https://v.gd',
        '1ptco': 'https://1pt.co'
    }
    
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service.upper()}: Available")
            else:
                print(f"⚠️ {service.upper()}: HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {service.upper()}: {e}")

if __name__ == "__main__":
    print("S3Drop URL Shortening Test Suite")
    print("This will test URL shortening services without using AWS.")
    print()
    
    try:
        # Test service availability first
        test_service_availability()
        
        # Test URL shortening
        results = test_url_shortening_services()
        
        print("\n🎉 Test completed!")
        
        working_count = sum(1 for r in results.values() if r['success'])
        total_count = len(results)
        
        if working_count == total_count:
            print("🎯 All URL shortening services are working!")
        elif working_count > 0:
            print(f"🎯 {working_count}/{total_count} URL shortening services are working.")
        else:
            print("⚠️ No URL shortening services are working. Check your internet connection.")
            
    except KeyboardInterrupt:
        print("\n👋 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
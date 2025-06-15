#!/usr/bin/env python3
"""
Quick API test script to debug the campaign view issue
"""

import requests
import sys
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def test_campaign_api():
    print("Testing Campaign API...")
    
    # Create session with retry strategy
    session = requests.Session()
    retry_strategy = Retry(total=3, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    
    base_url = "http://localhost:5000"
    
    try:
        # First, test if server is running
        print("1. Testing server connectivity...")
        response = session.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            print("   ✓ Server is running")
        else:
            print(f"   ✗ Server returned status: {response.status_code}")
            if "login" in response.url:
                print("   → Redirected to login (expected)")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Server connection failed: {e}")
        print("   → Make sure to start the server with: cd src && python app.py")
        return False
    
    # Test login and get session
    print("\n2. Testing login...")
    try:
        login_data = {
            'email': 'admin@company.com',
            'password': 'admin123'
        }
        response = session.post(f"{base_url}/login", data=login_data, timeout=5)
        if response.status_code == 200 and "dashboard" in response.url:
            print("   ✓ Login successful")
        else:
            print(f"   ✗ Login failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Login request failed: {e}")
        return False
    
    # Test campaign API
    print("\n3. Testing campaign API...")
    try:
        response = session.get(f"{base_url}/api/campaigns/1", timeout=5)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("   ✓ Campaign API working!")
            print(f"   Campaign: {data.get('name', 'Unknown')}")
            print(f"   Type: {data.get('type', 'Unknown')}")
            print(f"   Status: {data.get('status', 'Unknown')}")
            return True
        elif response.status_code == 403:
            print("   ✗ Authentication failed")
            print("   → Session might not be properly maintained")
            return False
        elif response.status_code == 404:
            print("   ✗ Campaign not found")
            return False
        else:
            print(f"   ✗ Unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ✗ API request failed: {e}")
        return False
    except ValueError as e:
        print(f"   ✗ JSON decode error: {e}")
        print(f"   Response text: {response.text[:200]}")
        return False

def main():
    print("=" * 50)
    print("Social Engineering Toolkit - API Test")
    print("=" * 50)
    
    success = test_campaign_api()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ API Test PASSED - Campaign view should work")
        print("\nIf you're still seeing issues:")
        print("1. Clear browser cache and cookies")
        print("2. Restart the application")
        print("3. Try logging out and logging back in")
    else:
        print("✗ API Test FAILED - Issues found")
        print("\nTo fix:")
        print("1. Make sure the server is running: cd src && python app.py")
        print("2. Check the console for error messages")
        print("3. Verify login credentials work")
    
    print("=" * 50)

if __name__ == '__main__':
    main()


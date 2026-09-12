import os
import sys
import urllib.request
import urllib.error
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.settings import SUPABASE_URL, SUPABASE_KEY


def test_supabase_rest():
    print(f"Testing Supabase REST API at: {SUPABASE_URL}")
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    # Try to fetch from a specific table
    url = f"{SUPABASE_URL}/rest/v1/stations?select=*"
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status_code = response.getcode()
            print(f"Status Code: {status_code}")
            if status_code == 200:
                print("Successfully connected to Supabase REST API via URL and KEY!")
                data = json.loads(response.read().decode())
                print(f"Response data: {data}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
        print(e.read().decode())
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")

if __name__ == "__main__":
    test_supabase_rest()

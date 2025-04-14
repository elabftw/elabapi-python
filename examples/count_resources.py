"""
DESCRIPTION:
This script counts the number of items in a specific resource category within an eLabFTW instance.
It fetches paginated data from the API and provides the total number of entries for the given category.

USAGE:
Run the script from the command line and pass the desired category ID as an argument:

    python count_resources.py <CATEGORY_ID>

Example:
    python count_resources.py 19

Make sure to set your API key and instance URL in the configuration section.
"""

import requests
import urllib3
import argparse

# ==========================
# 🔧 CONFIGURATION
# ==========================
API_HOST_URL = 'https://elab.local:3148/api/v2'  # <-- URL eLabFTW Goethe Uni or Replace with your instance URL 
API_KEY = 'apiKey4Test'  # <-- Replace with your API key

# Parse category_id from command-line argument
parser = argparse.ArgumentParser(description="Count entries in a specific resource category.")
parser.add_argument("category_id", type=int, help="Resource category ID to query")
args = parser.parse_args()

CATEGORY_ID = args.category_id

# Disable warnings for self-signed SSL certificates (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

# ==========================
# 📋 LIST RESOURCE CATEGORIES
# ==========================
print("📋 Loading resource categories (IDs only)...")

try:
    response = requests.get(f"{API_HOST_URL}/items_types", headers=headers, verify=False)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        categories = data.get("items", data.get("data", []))
    else:
        categories = data

    print("📂 Available category IDs:")
    for cat in categories:
        print(f"- Category ID: {cat.get('id')}")

except Exception as e:
    print(f"❌ Error while retrieving categories: {e}")

# ==========================
# 📊 COUNT ENTRIES
# ==========================
print(f"\n📊 Counting entries in category {CATEGORY_ID}...")

try:
    total_items = 0
    page = 1
    while True:
        response = requests.get(
            f"{API_HOST_URL}/items",
            headers=headers,
            params={"category_id": CATEGORY_ID, "page": page},
            verify=False
        )
        response.raise_for_status()
        items = response.json()

        if isinstance(items, dict):
            items = items.get("items", items.get("data", []))

        count = len(items)
        total_items += count

        if count < 50:
            break
        page += 1

    print(f"✅ Total entries in category {CATEGORY_ID}: {total_items}")

except Exception as e:
    print(f"❌ Error while counting items: {e}")

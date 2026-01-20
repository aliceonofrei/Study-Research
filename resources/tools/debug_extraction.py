#!/usr/bin/env python3
"""
Debug extraction to see why only 3 venues are extracted
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    url = "https://www.theknot.com/marketplace/wedding-reception-venues-seattle-wa?venue-amenities=uncovered-outdoor-wedding-reception-site+covered-outdoor-wedding-reception-site&sort=recommended"

    print("Opening The Knot page...")
    driver.get(url)
    time.sleep(10)

    venue_cards = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
    print(f"\nFound {len(venue_cards)} venue cards\n")
    print("="*80)

    for i, card in enumerate(venue_cards[:5], 1):  # Check first 5
        print(f"\nVENUE CARD #{i}")
        print("-"*80)

        # Try to extract name
        try:
            name_elem = card.find_element(By.CSS_SELECTOR, "[class*='vendor-name']")
            print(f"✅ Name: {name_elem.text}")
        except Exception as e:
            print(f"❌ Name extraction failed: {type(e).__name__}")

        # Try to extract location
        try:
            loc_elem = card.find_element(By.CSS_SELECTOR, "[class*='location-text']")
            print(f"✅ Location: {loc_elem.text}")
        except Exception as e:
            print(f"❌ Location extraction failed: {type(e).__name__}")

        # Try to extract rating
        try:
            rating_elem = card.find_element(By.CSS_SELECTOR, "[class*='star-count']")
            print(f"✅ Rating: {rating_elem.text}")
        except Exception as e:
            print(f"❌ Rating extraction failed: {type(e).__name__}")

        # Try to extract reviews
        try:
            reviews_elem = card.find_element(By.CSS_SELECTOR, "[class*='review-count']")
            print(f"✅ Reviews: {reviews_elem.text}")
        except Exception as e:
            print(f"❌ Reviews extraction failed: {type(e).__name__}")

    print("\n" + "="*80)
    print("\n⏸️  Browser will stay open for 30 seconds...")
    time.sleep(30)

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
    print("\n✅ Done!")

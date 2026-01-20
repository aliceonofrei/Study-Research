#!/usr/bin/env python3
"""
Test if The Knot uses infinite scroll for pagination
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # Wait for initial content
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
    )
    time.sleep(3)

    print("\n" + "="*80)
    print("TESTING INFINITE SCROLL")
    print("="*80)

    # Get initial count
    initial_venues = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
    initial_count = len(initial_venues)
    print(f"\nInitial venue count: {initial_count}")

    # Get first and last venue names
    first_venue = initial_venues[0].find_element(By.CSS_SELECTOR, "[class*='vendor-name']").text
    last_venue = initial_venues[-1].find_element(By.CSS_SELECTOR, "[class*='vendor-name']").text
    print(f"First venue: {first_venue}")
    print(f"Last venue: {last_venue}")

    # Try scrolling down multiple times
    print("\n" + "="*80)
    print("SCROLLING DOWN TO TRIGGER INFINITE SCROLL")
    print("="*80)

    for i in range(5):
        print(f"\nScroll attempt {i+1}/5:")

        # Scroll to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("  Scrolled to bottom, waiting 4 seconds...")
        time.sleep(4)

        # Check if more venues loaded
        current_venues = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
        current_count = len(current_venues)

        if current_count > initial_count:
            print(f"  ✅ New venues loaded! Count: {initial_count} → {current_count}")

            # Get new last venue
            new_last_venue = current_venues[-1].find_element(By.CSS_SELECTOR, "[class*='vendor-name']").text
            print(f"  New last venue: {new_last_venue}")

            initial_count = current_count
            last_venue = new_last_venue
        else:
            print(f"  ⚠️  No new venues loaded (still {current_count})")

    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    final_venues = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
    print(f"Final venue count: {len(final_venues)}")

    if len(final_venues) > 30:
        print("✅ Infinite scroll is working!")
    else:
        print("❌ Infinite scroll did not trigger - still at 30 venues")

    print("\n⏸️  Browser will stay open for 30 seconds for inspection...")
    time.sleep(30)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\n✅ Done!")

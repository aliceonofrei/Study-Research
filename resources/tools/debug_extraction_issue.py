#!/usr/bin/env python3
"""
Debug why only 3 venues are being extracted from 30 cards
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
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

    # Wait for content
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
    )
    time.sleep(3)

    print("\n" + "="*80)
    print("DEBUGGING VENUE EXTRACTION")
    print("="*80)

    venue_elements = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
    print(f"\nFound {len(venue_elements)} venue cards")

    successful = 0
    failed = 0

    for idx in range(min(10, len(venue_elements))):  # Check first 10
        print(f"\n--- Venue #{idx + 1} ---")

        # Re-query to avoid stale references
        venue_elements = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
        venue = venue_elements[idx]

        # Try to extract name
        try:
            name_elem = venue.find_element(By.CSS_SELECTOR, "[class*='vendor-name']")
            name = name_elem.text.strip()
            if name:
                print(f"✅ Name: {name}")
                successful += 1
            else:
                print(f"⚠️  Name element found but text is empty")
                failed += 1
        except NoSuchElementException:
            print(f"❌ Name element NOT found")
            failed += 1
        except Exception as e:
            print(f"❌ Error getting name: {e}")
            failed += 1

        # Try to extract location
        try:
            loc_elem = venue.find_element(By.CSS_SELECTOR, "[class*='location-text'] [class*='sr-only']")
            location = loc_elem.text.strip()
            print(f"   Location: {location}")
        except NoSuchElementException:
            print(f"   Location: Not found")
        except Exception as e:
            print(f"   Location error: {e}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Successful extractions (first 10): {successful}")
    print(f"Failed extractions (first 10): {failed}")

    if successful < 5:
        print("\n⚠️  WARNING: Low success rate suggests extraction issue!")
        print("This could be due to:")
        print("  - Changed HTML structure on The Knot")
        print("  - Slow page loading")
        print("  - Anti-bot detection blocking content")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\n✅ Done!")

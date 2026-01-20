#!/usr/bin/env python3
"""
Debug script to find pagination controls on The Knot
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup browser
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

try:
    url = "https://www.theknot.com/marketplace/wedding-reception-venues-seattle-wa?venue-amenities=uncovered-outdoor-wedding-reception-site+covered-outdoor-wedding-reception-site&sort=recommended"

    print("Opening The Knot page...")
    driver.get(url)

    print("Waiting 10 seconds for page to load...")
    time.sleep(10)

    print("\n" + "="*60)
    print("PAGINATION CONTROLS INSPECTION")
    print("="*60)

    # Scroll to bottom to make sure pagination is visible
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Try to find pagination with different selectors
    pagination_selectors = [
        ("Pagination nav", "nav[role='navigation']"),
        ("Pagination div", "[class*='pagination']"),
        ("Next button with aria-label", "button[aria-label*='next']"),
        ("Next button with aria-label", "button[aria-label*='Next']"),
        ("Next link with aria-label", "a[aria-label*='next']"),
        ("Next link with aria-label", "a[aria-label*='Next']"),
        ("Any button with 'next'", "button[class*='next']"),
        ("Any link with 'next'", "a[class*='next']"),
        ("Page number buttons", "button[aria-label*='page']"),
        ("Page number buttons", "button[aria-label*='Page']"),
        ("All navigation elements", "nav"),
        ("All buttons at bottom", "button"),
    ]

    print("\n🔍 Searching for pagination controls...\n")

    for desc, selector in pagination_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"✅ Found {len(elements)} elements: {desc} ({selector})")

                # Show details of first few elements
                for i, elem in enumerate(elements[:3]):
                    try:
                        aria_label = elem.get_attribute("aria-label")
                        elem_class = elem.get_attribute("class")
                        elem_text = elem.text[:50] if elem.text else "(no text)"
                        elem_tag = elem.tag_name

                        print(f"   [{i+1}] <{elem_tag}> aria-label='{aria_label}' class='{elem_class[:50]}...' text='{elem_text}'")
                    except:
                        pass
                print()
            else:
                print(f"❌ No elements: {desc} ({selector})")
        except Exception as e:
            print(f"❌ Error with {desc}: {e}")

    # Check current URL for page parameter
    print("\n" + "="*60)
    print("URL INSPECTION")
    print("="*60)
    print(f"Current URL: {driver.current_url}")

    # Try to find if it uses infinite scroll
    print("\n" + "="*60)
    print("SCROLL DETECTION")
    print("="*60)

    # Get initial number of venue cards
    initial_venues = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
    print(f"Initial venue count: {len(initial_venues)}")

    # Scroll down multiple times
    for i in range(3):
        print(f"\nScrolling down ({i+1}/3)...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        new_venues = driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
        print(f"Venue count after scroll: {len(new_venues)}")

        if len(new_venues) > len(initial_venues):
            print("✅ NEW VENUES LOADED - This site uses INFINITE SCROLL!")
            break
    else:
        print("❌ No new venues loaded from scrolling")

    print("\n⏸️  Browser will stay open for 30 seconds for manual inspection...")
    time.sleep(30)

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
    print("\n✅ Done!")

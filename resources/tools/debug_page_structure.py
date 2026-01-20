#!/usr/bin/env python3
"""
Debug script to inspect The Knot page structure
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup browser (visible so you can see what's happening)
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
    print("PAGE SOURCE INSPECTION")
    print("="*60)

    # Try to find venue cards with different selectors
    selectors_to_try = [
        "[data-testid='vendor-card']",
        ".vendor-card",
        ".vendorCard",
        "[class*='vendor']",
        "[class*='card']",
        "article",
        "[data-id]",
        "[data-vendor-id]",
    ]

    for selector in selectors_to_try:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            if elements:
                print(f"\n✅ Found {len(elements)} elements with selector: {selector}")
                if elements:
                    print(f"   Sample HTML: {elements[0].get_attribute('outerHTML')[:200]}...")
            else:
                print(f"❌ No elements found with: {selector}")
        except Exception as e:
            print(f"❌ Error with selector {selector}: {e}")

    # Save page source for inspection
    with open("page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("\n✅ Full page source saved to: page_source.html")
    print("   Open this file to inspect the HTML structure")

    print("\n⏸️  Browser will stay open for 30 seconds so you can inspect it...")
    print("   Look at the page and use browser DevTools (F12) to find venue cards")
    time.sleep(30)

except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
    print("\n✅ Done!")

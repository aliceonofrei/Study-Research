#!/usr/bin/env python3
"""
Detailed pagination debugging - inspect actual HTML and button attributes
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

    # Wait for page to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
    )
    time.sleep(3)

    # Scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    print("\n" + "="*80)
    print("PAGINATION BUTTONS DETAILED INSPECTION")
    print("="*80)

    # Find all buttons on the page
    all_buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"\nTotal buttons on page: {len(all_buttons)}")

    # Filter for pagination-related buttons
    pagination_buttons = []
    for btn in all_buttons:
        aria_label = btn.get_attribute("aria-label") or ""
        if "page" in aria_label.lower() or "next" in aria_label.lower() or "previous" in aria_label.lower():
            pagination_buttons.append(btn)

    print(f"Pagination-related buttons found: {len(pagination_buttons)}\n")

    for i, btn in enumerate(pagination_buttons, 1):
        aria_label = btn.get_attribute("aria-label")
        btn_class = btn.get_attribute("class")
        btn_text = btn.text
        is_disabled = btn.get_attribute("disabled")
        is_displayed = btn.is_displayed()

        print(f"Button #{i}:")
        print(f"  aria-label: {aria_label}")
        print(f"  class: {btn_class}")
        print(f"  text: '{btn_text}'")
        print(f"  disabled: {is_disabled}")
        print(f"  displayed: {is_displayed}")
        print()

    # Try to find navigation element
    print("="*80)
    print("PAGINATION CONTAINER INSPECTION")
    print("="*80)

    try:
        nav_elements = driver.find_elements(By.TAG_NAME, "nav")
        print(f"Found {len(nav_elements)} <nav> elements\n")

        for i, nav in enumerate(nav_elements, 1):
            aria_label = nav.get_attribute("aria-label") or "(none)"
            role = nav.get_attribute("role") or "(none)"
            nav_class = nav.get_attribute("class") or "(none)"

            # Get first 200 chars of inner HTML
            inner_html = nav.get_attribute("innerHTML")[:200] if nav.get_attribute("innerHTML") else "(empty)"

            print(f"Nav #{i}:")
            print(f"  aria-label: {aria_label}")
            print(f"  role: {role}")
            print(f"  class: {nav_class}")
            print(f"  innerHTML (first 200 chars): {inner_html}...")
            print()
    except Exception as e:
        print(f"Error inspecting nav: {e}")

    # Try clicking page 2 button
    print("="*80)
    print("ATTEMPTING TO CLICK PAGE 2")
    print("="*80)

    # Get first venue name before clicking
    try:
        first_venue = driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base'] [class*='vendor-name']")
        first_venue_name = first_venue.text
        print(f"First venue before click: {first_venue_name}")
    except:
        first_venue_name = "Unknown"
        print("Could not get first venue name")

    # Try different selectors for page 2
    selectors_to_try = [
        ("button[aria-label='Go to page 2']", "aria-label exact match"),
        ("button[aria-label*='page 2']", "aria-label contains 'page 2'"),
        ("button[aria-label*='Page 2']", "aria-label contains 'Page 2'"),
        ("[aria-label='Go to page 2']", "any element with aria-label"),
        ("button:nth-child(2)", "second button in pagination"),
    ]

    clicked = False
    for selector, description in selectors_to_try:
        try:
            print(f"\nTrying: {description} ({selector})")
            # Look within nav elements
            for nav in nav_elements:
                try:
                    btn = nav.find_element(By.CSS_SELECTOR, selector)
                    print(f"  ✅ Found button in nav!")
                    print(f"     aria-label: {btn.get_attribute('aria-label')}")
                    print(f"     Clicking...")

                    # Get reference to first venue element for staleness check
                    first_venue_elem = driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")

                    driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1)

                    # Check if element became stale
                    try:
                        first_venue_elem.get_attribute("class")
                        print(f"  ⚠️  Element NOT stale - page didn't refresh")
                    except:
                        print(f"  ✅ Element became stale - page refreshed!")

                    # Wait for new content
                    time.sleep(3)

                    # Get new first venue name
                    try:
                        new_first_venue = driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base'] [class*='vendor-name']")
                        new_first_venue_name = new_first_venue.text
                        print(f"  First venue after click: {new_first_venue_name}")

                        if new_first_venue_name != first_venue_name:
                            print(f"  ✅ SUCCESS! Venue changed, we're on page 2!")
                            clicked = True
                            break
                        else:
                            print(f"  ❌ First venue didn't change")
                    except Exception as e:
                        print(f"  Error getting new venue: {e}")

                    if clicked:
                        break
                except:
                    continue

            if clicked:
                break

        except Exception as e:
            print(f"  ❌ Failed: {e}")

    if not clicked:
        print("\n❌ Could not successfully navigate to page 2 with any selector")

    # Check current URL
    print("\n" + "="*80)
    print("CURRENT URL")
    print("="*80)
    print(driver.current_url)

    print("\n⏸️  Browser will stay open for 60 seconds for manual inspection...")
    time.sleep(60)

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

finally:
    driver.quit()
    print("\n✅ Done!")

#!/usr/bin/env python3
"""
Wedding Venue Scraper for The Knot

This script scrapes wedding venue data from TheKnot.com for multiple cities,
specifically targeting outdoor wedding venues (covered and uncovered).

Data collected:
- Venue name
- Location
- Rating
- Number of reviews
- City/Area information

Author: AI-Assisted
Date: 2026-01-20
"""

import time
import csv
import re
import os
from typing import List, Dict, Optional
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


class TheKnotVenueScraper:
    """Scraper for The Knot wedding venue listings"""

    BASE_URL = "https://www.theknot.com/marketplace/wedding-reception-venues-{}-{}?venue-amenities=uncovered-outdoor-wedding-reception-site+covered-outdoor-wedding-reception-site&sort=recommended"

    # Only the 14 cities that were missed due to formatting issues
    CITIES = [
        ("St. Paul", "MN"),
        ("St. Louis", "MO"),
        ("St. Petersburg", "FL"),
        ("Boise City", "ID"),
        ("Port St. Lucie", "FL"),
        ("Grand Rapids", "MI"),
        ("Sioux Falls", "SD"),
        ("Fort Collins", "CO"),
        ("El Cajon", "CA"),
        ("Federal Way", "WA"),
        ("St. George", "UT"),
        ("O'Fallon", "MO"),
        ("Johns Creek", "GA"),
        ("Parma", "OH")
    ]

    def __init__(self, headless: bool = True):
        """Initialize the scraper with Chrome WebDriver"""
        self.headless = headless
        self.driver = None
        self.all_venues = []

    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless=new")

        # Additional options for stability and performance
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def format_city_url(self, city: str, state: str) -> str:
        """Format city and state for The Knot URL structure"""
        city_formatted = city.lower()

        # Handle special formatting cases
        # Replace "St." with "saint"
        city_formatted = city_formatted.replace("st. ", "saint-")

        # Handle "Boise City" -> "boise"
        if city_formatted == "boise city":
            city_formatted = "boise"

        # Convert spaces to hyphens
        city_formatted = city_formatted.replace(" ", "-")

        # Remove apostrophes (O'Fallon -> ofallon)
        city_formatted = city_formatted.replace("'", "")

        # Remove periods
        city_formatted = city_formatted.replace(".", "")

        state_formatted = state.lower()

        return self.BASE_URL.format(city_formatted, state_formatted)

    def wait_for_page_load(self, timeout: int = 15):
        """Wait for venue cards to load on the page"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
            )
            time.sleep(2)  # Additional wait for dynamic content
            return True
        except TimeoutException:
            print(f"  ⚠️  Timeout waiting for venues to load")
            return False

    def trigger_lazy_loading(self):
        """Scroll through page to trigger lazy loading of all venue content"""
        try:
            print(f"  ⏳ Pre-scrolling to trigger lazy loading...", end='', flush=True)

            # Get all venue cards
            venue_elements = self.driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")

            if not venue_elements:
                print(f" no venues found")
                return

            # Scroll through venues in batches to trigger lazy loading
            # Don't need to scroll every single one, just enough to trigger all loading
            batch_size = 10
            batches_scrolled = 0
            for i in range(0, len(venue_elements), batch_size):
                try:
                    # Re-query to avoid stale references
                    current_venues = self.driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
                    if i < len(current_venues):
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", current_venues[i])
                        time.sleep(0.5)  # Wait longer for loading
                        batches_scrolled += 1
                except:
                    continue

            # Scroll to bottom to ensure everything loaded
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)

            # Scroll back to top
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            print(f" done ({batches_scrolled} batches)")

        except Exception as e:
            print(f" failed: {e}")
            # If this fails, it's not critical - individual venue scrolling will handle it
            pass

    def extract_venue_data(self, venue_element) -> Optional[Dict]:
        """Extract data from a single venue card"""
        try:
            venue_data = {
                'name': '',
                'location': '',
                'rating': '',
                'num_reviews': '',
                'city_area': ''
            }

            # Extract venue name
            try:
                name_element = venue_element.find_element(By.CSS_SELECTOR, "[class*='vendor-name']")
                venue_data['name'] = name_element.text.strip()
            except NoSuchElementException:
                pass

            # Extract location (prefer sr-only for full text, fallback to visible text)
            try:
                # Try to get full location from sr-only span first
                location_element = venue_element.find_element(By.CSS_SELECTOR, "[class*='location-text'] [class*='sr-only']")
                venue_data['location'] = location_element.text.strip()
            except NoSuchElementException:
                try:
                    # Fallback: get visible location text but remove sr-only content
                    location_container = venue_element.find_element(By.CSS_SELECTOR, "[class*='location-text']")
                    # Get all text, but filter out aria-hidden elements
                    try:
                        visible_text = location_container.find_element(By.CSS_SELECTOR, "[aria-hidden='true']")
                        venue_data['location'] = visible_text.text.strip()
                    except NoSuchElementException:
                        venue_data['location'] = location_container.text.strip()
                except NoSuchElementException:
                    pass

            # Extract rating
            try:
                rating_element = venue_element.find_element(By.CSS_SELECTOR, "[class*='star-count']")
                rating_text = rating_element.text.strip()
                # Extract numeric rating (e.g., "4.9" from "4.9Stars")
                rating_match = re.search(r'(\d+\.?\d*)', rating_text)
                if rating_match:
                    venue_data['rating'] = rating_match.group(1)
            except NoSuchElementException:
                pass

            # Extract number of reviews
            try:
                reviews_element = venue_element.find_element(By.CSS_SELECTOR, "[class*='review-count']")
                reviews_text = reviews_element.text.strip()
                # Extract number (e.g., "74" from "(74)")
                reviews_match = re.search(r'\(?\s*(\d+)\s*\)?', reviews_text)
                if reviews_match:
                    venue_data['num_reviews'] = reviews_match.group(1)
            except NoSuchElementException:
                pass

            # Extract city/area from location if it's a broader area
            if venue_data['location']:
                # Try to identify if location contains multiple cities or is a region
                location_parts = venue_data['location'].split(',')
                if len(location_parts) >= 2:
                    venue_data['city_area'] = location_parts[0].strip()

            return venue_data if venue_data['name'] else None

        except Exception as e:
            print(f"  ❌ Error extracting venue data: {e}")
            return None

    def get_venues_on_page(self, retry_count: int = 0, max_retries: int = 2) -> List[Dict]:
        """Extract all venues from the current page with retry logic"""
        venues = []

        try:
            # Wait a moment for page to fully render
            time.sleep(1)

            # Trigger lazy loading by scrolling through page
            self.trigger_lazy_loading()

            # Get count of venue cards
            venue_elements = self.driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
            total_venues = len(venue_elements)

            print(f"  Found {total_venues} venue cards on page")
            print(f"  Extracting venue data...", end='', flush=True)

            # Extract data from each venue by re-querying each time
            # This avoids stale element references
            for idx in range(total_venues):
                try:
                    # Re-find all venue elements each iteration to avoid stale references
                    current_venue_elements = self.driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")

                    if idx < len(current_venue_elements):
                        venue_elem = current_venue_elements[idx]

                        # CRITICAL: Scroll venue into view to trigger lazy loading
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", venue_elem)
                        time.sleep(0.5)  # Brief wait for content to load

                        venue_data = self.extract_venue_data(venue_elem)
                        if venue_data:
                            venues.append(venue_data)

                    # Show progress every 10 venues
                    if (idx + 1) % 10 == 0 or (idx + 1) == total_venues:
                        print(f"\r  Extracting venue data... {idx + 1}/{total_venues}", end='', flush=True)

                except StaleElementReferenceException:
                    # Re-query and try again once
                    try:
                        current_venue_elements = self.driver.find_elements(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
                        if idx < len(current_venue_elements):
                            venue_elem = current_venue_elements[idx]

                            # Scroll into view for lazy loading
                            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", venue_elem)
                            time.sleep(0.5)

                            venue_data = self.extract_venue_data(venue_elem)
                            if venue_data:
                                venues.append(venue_data)
                    except:
                        continue

            print()  # New line after progress

        except TimeoutException as e:
            print(f"\n  ⏱️  Timeout during venue extraction: {e}")

            # Retry if we haven't exceeded max retries
            if retry_count < max_retries:
                wait_time = 3 * (retry_count + 1)  # 3s, 6s
                print(f"  ⏳ Waiting {wait_time}s before retry {retry_count + 1}/{max_retries}...")
                time.sleep(wait_time)

                # Refresh the page to clear any hanging state
                try:
                    print(f"  🔄 Refreshing page...")
                    self.driver.refresh()
                    time.sleep(3)
                    return self.get_venues_on_page(retry_count + 1, max_retries)
                except Exception as refresh_error:
                    print(f"  ❌ Failed to refresh page: {refresh_error}")
                    return venues
            else:
                print(f"  ⚠️  Max retries exceeded for this page, continuing with {len(venues)} venues")
                return venues

        except Exception as e:
            # Check if it's a timeout-related error
            if "timeout" in str(e).lower() or "timed out" in str(e).lower():
                print(f"\n  ⏱️  Timeout during venue extraction: {e}")

                if retry_count < max_retries:
                    wait_time = 3 * (retry_count + 1)
                    print(f"  ⏳ Waiting {wait_time}s before retry {retry_count + 1}/{max_retries}...")
                    time.sleep(wait_time)

                    try:
                        print(f"  🔄 Refreshing page...")
                        self.driver.refresh()
                        time.sleep(3)
                        return self.get_venues_on_page(retry_count + 1, max_retries)
                    except Exception as refresh_error:
                        print(f"  ❌ Failed to refresh page: {refresh_error}")
                        return venues
                else:
                    print(f"  ⚠️  Max retries exceeded for this page, continuing with {len(venues)} venues")
                    return venues
            else:
                print(f"\n  ❌ Error getting venues: {e}")
                return venues

        return venues

    def try_click_button(self, button, method_name: str) -> bool:
        """Try clicking a button using a specific method and verify the page changed"""
        try:
            # Get reference to first venue element (not just text) for staleness detection
            original_venue_name = ""
            first_venue_elem = None

            try:
                first_venue_elem = self.driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
                original_venue_name = first_venue_elem.find_element(By.CSS_SELECTOR, "[class*='vendor-name']").text.strip()
            except (NoSuchElementException, StaleElementReferenceException):
                # If we can't get the original venue, that's okay - we'll just check for staleness
                pass

            # Perform the click
            try:
                if method_name == "javascript":
                    self.driver.execute_script("arguments[0].click();", button)
                elif method_name == "action_chains":
                    actions = ActionChains(self.driver)
                    actions.move_to_element(button).click().perform()
                elif method_name == "regular":
                    button.click()
            except StaleElementReferenceException:
                print(f"    ⚠️  Button became stale before {method_name} click")
                return False

            print(f"    ⏳ Clicked with {method_name}, waiting for DOM update...")

            # Wait for the element to become stale (indicating page updated)
            page_changed = False
            if first_venue_elem:
                try:
                    WebDriverWait(self.driver, 10).until(EC.staleness_of(first_venue_elem))
                    print(f"    ✓ DOM updated (element became stale)")
                    page_changed = True
                except TimeoutException:
                    print(f"    ⚠️  Element didn't become stale after {method_name} click")
                except StaleElementReferenceException:
                    # Element is already stale, which is actually good - means page updated
                    print(f"    ✓ DOM updated (element already stale)")
                    page_changed = True

            # If page changed, wait for new venue cards to load
            if page_changed:
                try:
                    # Wait up to 10 seconds for new venue cards to appear
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
                    )
                    time.sleep(2)  # Additional wait for content to fully render
                except TimeoutException:
                    print(f"    ⚠️  New venue cards didn't load after {method_name} click")
                    return False

            # Verify content actually changed by comparing venue names
            try:
                new_first_venue = self.driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base'] [class*='vendor-name']")
                new_venue_name = new_first_venue.text.strip()

                if original_venue_name and new_venue_name and new_venue_name != original_venue_name:
                    print(f"    ✅ Success! Page changed ('{original_venue_name[:25]}...' → '{new_venue_name[:25]}...')")
                    return True
                elif not original_venue_name and page_changed:
                    # If we couldn't get original name but page changed, assume success if we found new venues
                    print(f"    ✅ Success! Found venues on new page")
                    return True
                else:
                    print(f"    ⚠️  First venue unchanged with {method_name}: '{original_venue_name[:30]}...'")
                    return False
            except (NoSuchElementException, StaleElementReferenceException) as e:
                print(f"    ⚠️  Could not verify change with {method_name}: {e}")
                return False

        except Exception as e:
            print(f"    ❌ Error with {method_name}: {e}")
            return False

    def click_next_page(self, current_page: int, seen_venue_keys: set) -> bool:
        """Navigate to the next page using multiple strategies"""
        try:
            # Scroll to bottom first to ensure pagination is visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            next_page_num = current_page + 1

            # Strategy 1: Try multiple button selector variations
            button_selectors = [
                f"a[aria-label='Go to page {next_page_num}']",
                f"button[aria-label='Go to page {next_page_num}']",
                f"a[aria-label='Page {next_page_num}']",
                f"button[aria-label='Page {next_page_num}']",
                f"button[aria-label='page {next_page_num}']",
                f"button[aria-label*='page {next_page_num}']",
            ]

            page_button = None
            for selector in button_selectors:
                try:
                    page_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"  🔍 Found button: {selector}")
                    break
                except NoSuchElementException:
                    continue

            if page_button:
                # Scroll button into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page_button)
                time.sleep(1)

                # Try different click methods until one works
                click_methods = ["action_chains", "javascript", "regular"]
                for method in click_methods:
                    if self.try_click_button(page_button, method):
                        # Wait for page to fully load
                        time.sleep(2)
                        WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
                        )
                        return True

                print(f"  ⚠️  All click methods failed - page didn't change")

            # Strategy 2: Try "Next" button
            if not page_button or True:  # Always try this as fallback
                next_button_selectors = [
                    "a[aria-label='Go to next page']",
                    "button[aria-label='Go to next page']",
                    "button[aria-label='Next page']",
                    "button[aria-label*='Next']",
                    "a[aria-label*='Next']",
                ]

                next_button = None
                for selector in next_button_selectors:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"  🔍 Found 'Next' button: {selector}")
                        break
                    except NoSuchElementException:
                        continue

                if next_button:
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                    time.sleep(1)

                    click_methods = ["action_chains", "javascript", "regular"]
                    for method in click_methods:
                        if self.try_click_button(next_button, method):
                            time.sleep(2)
                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
                            )
                            return True

            # Strategy 3: Try URL-based pagination
            print(f"  🔍 Trying URL-based navigation...")
            current_url = self.driver.current_url

            url_params_to_try = [
                f"&page={next_page_num}",
                f"&p={next_page_num}",
                f"&offset={(next_page_num - 1) * 30}",
            ]

            for param in url_params_to_try:
                # Check if URL already has query params
                if '?' in current_url:
                    base_url = current_url.split('&page=')[0].split('&p=')[0].split('&offset=')[0]
                    new_url = base_url + param
                else:
                    new_url = current_url + param.replace('&', '?')

                print(f"  ⏳ Trying: {new_url[:80]}...")

                # Get first venue before navigation
                try:
                    original_venue = self.driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base'] [class*='vendor-name']")
                    original_name = original_venue.text.strip()
                except:
                    original_name = ""

                self.driver.get(new_url)
                time.sleep(4)

                # Check if it worked
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
                    )

                    new_venue_elem = self.driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
                    new_venue_name = new_venue_elem.find_element(By.CSS_SELECTOR, "[class*='vendor-name']").text.strip()

                    # Get location too for better verification
                    try:
                        new_venue_location = new_venue_elem.find_element(By.CSS_SELECTOR, "[class*='location-text'] [class*='sr-only']").text.strip()
                    except:
                        new_venue_location = ""

                    new_venue_key = (new_venue_name, new_venue_location)

                    # Check if content changed AND we haven't seen this venue before
                    if original_name and new_venue_name and new_venue_name != original_name:
                        if new_venue_key in seen_venue_keys:
                            print(f"  ⚠️  First venue is a duplicate - navigation looped back!")
                            print(f"      Venue: '{new_venue_name[:40]}...'")
                            continue  # Try next URL parameter
                        else:
                            print(f"  ✅ URL navigation worked! ('{original_name[:25]}...' → '{new_venue_name[:25]}...')")
                            return True
                except:
                    continue

            print(f"  ℹ️  All pagination methods failed - assuming last page")
            return False

        except Exception as e:
            print(f"  ⚠️  Error navigating to next page: {e}")
            return False

    def get_alternative_city_names(self, city: str) -> List[str]:
        """Generate alternative spellings for a city name

        This generates variations that will produce DIFFERENT URLs after format_city_url processes them
        """
        alternatives = []

        # For apostrophes (O'Fallon, Lee's Summit)
        if "'" in city:
            # Remove apostrophe: O'Fallon -> OFallon
            no_apostrophe = city.replace("'", "")
            alternatives.append(no_apostrophe)

            # Replace apostrophe with space: O'Fallon -> O Fallon (becomes o-fallon in URL)
            with_space = city.replace("'", " ")
            alternatives.append(with_space)

            # Replace apostrophe with hyphen directly
            with_hyphen = city.replace("'", "-")
            alternatives.append(with_hyphen)

        # For "St." variations (St. Louis, St. Paul, St. Petersburg, St. George, Port St. Lucie)
        if "St." in city:
            # Try "Saint" (full word)
            alternatives.append(city.replace("St.", "Saint"))

            # Try "St" without period
            alternatives.append(city.replace("St.", "St"))

        # For "Saint" (if someone passes it that way)
        if "Saint" in city and "St." not in city:
            alternatives.append(city.replace("Saint", "St."))
            alternatives.append(city.replace("Saint", "St"))

        # For "Fort" (Fort Collins, Fort Wayne, etc.)
        if city.startswith("Fort "):
            alternatives.append(city.replace("Fort ", "Ft. "))
            alternatives.append(city.replace("Fort ", "Ft "))

        # For "El" prefix (El Cajon)
        if city.startswith("El "):
            # Try without space: "El Cajon" -> "ElCajon" -> "elcajon" in URL
            alternatives.append(city.replace("El ", "El"))
            # Try just the second part: "El Cajon" -> "Cajon"
            alternatives.append(city[3:])  # Remove "El "

        # For multi-word cities - try without hyphen/space
        if " " in city and "'" not in city:
            # Remove all spaces: "Grand Rapids" -> "GrandRapids" -> "grandrapids" in URL
            alternatives.append(city.replace(" ", ""))

        # For "Johns Creek" specifically - try with apostrophe
        if city == "Johns Creek":
            alternatives.append("John's Creek")
            alternatives.append("JohnsCreek")

        # For "Federal Way" - try without space
        if city == "Federal Way":
            alternatives.append("FederalWay")

        # For "Grand Rapids" - try without space
        if city == "Grand Rapids":
            alternatives.append("GrandRapids")

        # For "Sioux Falls" - try without space
        if city == "Sioux Falls":
            alternatives.append("SiouxFalls")

        # Special case: Boise City
        if city == "Boise City":
            alternatives.append("Boise")
        if city == "Boise":
            alternatives.append("Boise City")

        # For "Parma" - try common misspellings
        if city == "Parma":
            alternatives.append("Parma Heights")

        # Remove duplicates while preserving order
        seen = set()
        unique_alternatives = []
        for alt in alternatives:
            if alt != city and alt not in seen:
                seen.add(alt)
                unique_alternatives.append(alt)

        return unique_alternatives

    def scrape_city(self, city: str, state: str, retry_count: int = 0, max_retries: int = 3) -> List[Dict]:
        """Scrape all venues for a given city with retry logic"""
        print(f"\n🔍 Scraping {city}, {state}..." + (f" (retry {retry_count}/{max_retries})" if retry_count > 0 else ""))

        url = self.format_city_url(city, state)
        print(f"  🌐 URL: {url}")
        city_venues = []
        seen_venue_keys = set()  # Track (name, location) tuples to detect duplicates/loops
        page_num = 1
        max_duplicate_pages = 2  # Stop if we see 2 consecutive pages with all duplicates

        try:
            self.driver.get(url)

            if not self.wait_for_page_load():
                print(f"  ⚠️  No venues found for {city}, {state}")

                # IMPORTANT: Try alternatives even when no venues found!
                if retry_count == 0:  # Only try alternatives on first attempt
                    alternatives = self.get_alternative_city_names(city)
                    if alternatives:
                        print(f"  🔄 No results with '{city}' - trying alternative spellings...")

                        for alt_city in alternatives:
                            print(f"  🔄 Trying alternative: {alt_city}, {state}")
                            alt_venues = self.scrape_city(alt_city, state, retry_count=999, max_retries=999)  # High retry_count to skip alternative checking

                            if alt_venues:  # If we found venues with this alternative
                                print(f"     ✅ Found {len(alt_venues)} venues with '{alt_city}' - using this version!")
                                return alt_venues
                            else:
                                print(f"     No venues found with '{alt_city}'")

                        print(f"  ⚠️  No results found with any spelling variation")

                return city_venues  # Return empty list

            consecutive_duplicate_pages = 0

            while True:
                print(f"  📄 Processing page {page_num}...")

                # Get venues from current page
                venues = self.get_venues_on_page()

                # Track how many new venues we found on this page
                new_venues_count = 0

                # Add venues, but track duplicates to detect loops
                for venue in venues:
                    venue_key = (venue.get('name', ''), venue.get('location', ''))

                    # Always add the venue (user will handle deduplication)
                    venue['search_city'] = city
                    venue['search_state'] = state
                    city_venues.append(venue)

                    # But track if it's new for loop detection
                    if venue_key not in seen_venue_keys:
                        new_venues_count += 1
                        seen_venue_keys.add(venue_key)

                print(f"  ✅ Extracted {len(venues)} venues from page {page_num} ({new_venues_count} new, {len(venues) - new_venues_count} duplicates)")

                # If we got mostly duplicates, we might be in a loop
                if len(venues) > 0 and new_venues_count == 0:
                    consecutive_duplicate_pages += 1
                    print(f"  ⚠️  All venues were duplicates (loop detection: {consecutive_duplicate_pages}/{max_duplicate_pages})")

                    if consecutive_duplicate_pages >= max_duplicate_pages:
                        print(f"  ⚠️  Detected pagination loop - stopping")
                        break
                else:
                    consecutive_duplicate_pages = 0

                # Wait for page to settle after all the scrolling during extraction
                time.sleep(2)

                # Try to go to next page
                if not self.click_next_page(page_num, seen_venue_keys):
                    print(f"  ✅ Reached last page")
                    break

                page_num += 1

                # Safety limit to prevent infinite loops
                if page_num > 50:
                    print(f"  ⚠️  Reached page limit (50)")
                    break

            print(f"✅ Total venues found for {city}, {state}: {len(city_venues)}")
            print(f"   Unique venues: {len(seen_venue_keys)}")

            # If we got very few results, try alternative spellings
            if len(seen_venue_keys) < 5 and retry_count == 0:  # Only try alternatives on first attempt
                alternatives = self.get_alternative_city_names(city)
                if alternatives:
                    print(f"  ⚠️  Low result count ({len(seen_venue_keys)} venues) - trying alternative spellings...")

                    best_results = city_venues
                    best_count = len(seen_venue_keys)
                    best_city_name = city

                    for alt_city in alternatives:
                        print(f"  🔄 Trying alternative: {alt_city}, {state}")
                        alt_venues = self.scrape_city(alt_city, state, retry_count=999, max_retries=999)  # High retry_count to skip alternative checking

                        # Count unique venues in alternative results
                        alt_unique = set()
                        for venue in alt_venues:
                            venue_key = (venue.get('name', ''), venue.get('location', ''))
                            alt_unique.add(venue_key)

                        print(f"     Found {len(alt_unique)} unique venues with '{alt_city}'")

                        if len(alt_unique) > best_count:
                            best_results = alt_venues
                            best_count = len(alt_unique)
                            best_city_name = alt_city
                            print(f"     ✅ Better results with '{alt_city}' - using this version")

                    # Use the best results
                    if best_city_name != city:
                        print(f"  ✅ Using results from '{best_city_name}' ({best_count} venues vs {len(seen_venue_keys)})")
                        return best_results
                    else:
                        print(f"  ℹ️  Original spelling '{city}' had the best results")

        except TimeoutException as e:
            print(f"⏱️  Timeout error for {city}, {state}: {e}")

            # Retry if we haven't exceeded max retries
            if retry_count < max_retries:
                wait_time = 5 * (retry_count + 1)  # Exponential backoff: 5s, 10s, 15s
                print(f"  ⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

                # Restart browser to clear any hanging state
                try:
                    print(f"  🔄 Restarting browser...")
                    self.close()
                    self.setup_driver()
                    return self.scrape_city(city, state, retry_count + 1, max_retries)
                except Exception as restart_error:
                    print(f"  ❌ Failed to restart browser: {restart_error}")
                    return city_venues
            else:
                print(f"  ❌ Max retries exceeded for {city}, {state}")
                return city_venues

        except Exception as e:
            print(f"❌ Error scraping {city}, {state}: {e}")

            # For other errors, try to recover by restarting browser
            # Handle: timeouts, crashes, and connection errors
            error_str = str(e).lower()
            should_retry = (
                "timeout" in error_str or
                "timed out" in error_str or
                "crash" in error_str or
                "connection" in error_str
            )

            if retry_count < max_retries and should_retry:
                wait_time = 5 * (retry_count + 1)
                print(f"  ⏳ Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)

                try:
                    print(f"  🔄 Restarting browser...")
                    self.close()
                    self.setup_driver()
                    return self.scrape_city(city, state, retry_count + 1, max_retries)
                except Exception as restart_error:
                    print(f"  ❌ Failed to restart browser: {restart_error}")
                    return city_venues

        return city_venues

    def load_existing_data(self, filename: str) -> set:
        """Load existing CSV and return set of already-scraped cities"""
        already_scraped = set()

        try:
            if not os.path.exists(filename):
                print(f"📄 No existing file found at {filename}")
                return already_scraped

            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                venues_loaded = 0

                for row in reader:
                    city = row.get('search_city', '')
                    state = row.get('search_state', '')
                    if city and state:
                        already_scraped.add((city, state))
                        self.all_venues.append(row)
                        venues_loaded += 1

                print(f"✅ Loaded {venues_loaded} existing venues from {filename}")
                print(f"✅ Already scraped {len(already_scraped)} cities")

        except Exception as e:
            print(f"⚠️  Error loading existing data: {e}")

        return already_scraped

    def save_incrementally(self, filename: str):
        """Save current data immediately (auto-save after each city)"""
        try:
            if not self.all_venues:
                return

            fieldnames = ['search_city', 'search_state', 'name', 'location', 'city_area', 'rating', 'num_reviews']

            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for venue in self.all_venues:
                    writer.writerow(venue)

            # Silent save - no output to avoid cluttering logs

        except Exception as e:
            print(f"⚠️  Auto-save failed: {e}")

    def scrape_all_cities(self, start_index: int = 0, limit: Optional[int] = None, output_file: str = "wedding_venues_outdoor_data.csv"):
        """Scrape venues for all cities with auto-save after each city"""
        print(f"🚀 Starting scrape for {len(self.CITIES)} cities...")
        print(f"⏰ This may take several hours to complete")
        print(f"💾 Auto-save enabled: Data saved after every city to {output_file}")

        # Load existing data if file exists
        already_scraped = self.load_existing_data(output_file)

        cities_to_scrape = self.CITIES[start_index:start_index + limit] if limit else self.CITIES[start_index:]

        for idx, (city, state) in enumerate(cities_to_scrape, start=start_index + 1):
            # Skip if already scraped
            if (city, state) in already_scraped:
                print(f"\n{'='*60}")
                print(f"Progress: {idx}/{len(self.CITIES)} cities")
                print(f"{'='*60}")
                print(f"⏭️  Skipping {city}, {state} (already scraped)")
                continue

            print(f"\n{'='*60}")
            print(f"Progress: {idx}/{len(self.CITIES)} cities")
            print(f"{'='*60}")

            city_venues = self.scrape_city(city, state)
            self.all_venues.extend(city_venues)

            # Show cumulative progress
            print(f"📈 Total venues collected so far: {len(self.all_venues)}")

            # AUTO-SAVE after every city
            print(f"💾 Auto-saving to {output_file}...")
            self.save_incrementally(output_file)
            print(f"✅ Saved! Safe to stop anytime with Ctrl+C")

        print(f"\n🎉 Scraping complete! Total venues collected: {len(self.all_venues)}")


    def export_to_csv(self, filename: str = "wedding_venues_data.csv"):
        """Export collected venue data to CSV"""
        if not self.all_venues:
            print("❌ No venue data to export")
            return

        fieldnames = ['search_city', 'search_state', 'name', 'location', 'city_area', 'rating', 'num_reviews']

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for venue in self.all_venues:
                writer.writerow(venue)

        print(f"✅ Data exported to {filename}")
        print(f"📊 Total venues: {len(self.all_venues)}")

    def close(self):
        """Close the browser driver"""
        if self.driver:
            self.driver.quit()
            print("✅ Browser closed")


def main():
    """Main execution function"""
    print("\n" + "=" * 60)
    print("🏞️  THE KNOT - OUTDOOR WEDDING VENUE SCRAPER")
    print("=" * 60)
    print("📋 Scraping outdoor venues (covered + uncovered)")
    print("💾 Output: wedding_venues_outdoor_data.csv")
    print("=" * 60)

    scraper = TheKnotVenueScraper(headless=True)

    try:
        scraper.setup_driver()

        # For testing, you can limit the number of cities:
        # scraper.scrape_all_cities(start_index=0, limit=3, output_file="wedding_venues_outdoor_data.csv")

        # Scrape all cities with auto-save
        scraper.scrape_all_cities(
            start_index=0,
            output_file="wedding_venues_outdoor_data.csv"
        )

    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print(f"💾 Data already saved via auto-save: {len(scraper.all_venues)} venues")

    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")

    finally:
        scraper.close()


if __name__ == "__main__":
    main()

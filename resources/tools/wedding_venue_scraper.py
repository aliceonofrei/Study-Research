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
from typing import List, Dict, Optional
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

    # List of all cities to scrape
    CITIES = [
        ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
        ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
        ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
        ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("Indianapolis", "IN"),
        ("San Francisco", "CA"), ("Seattle", "WA"), ("Denver", "CO"), ("Oklahoma City", "OK"),
        ("Nashville", "TN"), ("El Paso", "TX"), ("Washington", "DC"), ("Boston", "MA"),
        ("Las Vegas", "NV"), ("Portland", "OR"), ("Detroit", "MI"), ("Memphis", "TN"),
        ("Louisville", "KY"), ("Baltimore", "MD"), ("Milwaukee", "WI"), ("Albuquerque", "NM"),
        ("Fresno", "CA"), ("Tucson", "AZ"), ("Sacramento", "CA"), ("Kansas City", "MO"),
        ("Mesa", "AZ"), ("Atlanta", "GA"), ("Omaha", "NE"), ("Colorado Springs", "CO"),
        ("Raleigh", "NC"), ("Long Beach", "CA"), ("Virginia Beach", "VA"), ("Miami", "FL"),
        ("Oakland", "CA"), ("Minneapolis", "MN"), ("Tulsa", "OK"), ("Bakersfield", "CA"),
        ("Wichita", "KS"), ("Arlington", "TX"), ("Tampa", "FL"), ("Aurora", "CO"),
        ("New Orleans", "LA"), ("Cleveland", "OH"), ("Honolulu", "HI"), ("Anaheim", "CA"),
        ("Henderson", "NV"), ("Lexington", "KY"), ("Stockton", "CA"), ("Corpus Christi", "TX"),
        ("Riverside", "CA"), ("Orlando", "FL"), ("Santa Ana", "CA"), ("Cincinnati", "OH"),
        ("Irvine", "CA"), ("St. Paul", "MN"), ("Newark", "NJ"), ("Pittsburgh", "PA"),
        ("Greensboro", "NC"), ("St. Louis", "MO"), ("Lincoln", "NE"), ("Jersey City", "NJ"),
        ("Anchorage", "AK"), ("Durham", "NC"), ("Plano", "TX"), ("Chandler", "AZ"),
        ("Buffalo", "NY"), ("Madison", "WI"), ("Chula Vista", "CA"), ("Gilbert", "AZ"),
        ("North Las Vegas", "NV"), ("Reno", "NV"), ("Toledo", "OH"), ("Fort Wayne", "IN"),
        ("Lubbock", "TX"), ("St. Petersburg", "FL"), ("Laredo", "TX"), ("Irving", "TX"),
        ("Chesapeake", "VA"), ("Winston-Salem", "NC"), ("Glendale", "AZ"), ("Garland", "TX"),
        ("Scottsdale", "AZ"), ("Boise City", "ID"), ("Norfolk", "VA"), ("Spokane", "WA"),
        ("Santa Clarita", "CA"), ("Fremont", "CA"), ("Richmond", "VA"), ("Baton Rouge", "LA"),
        ("Hialeah", "FL"), ("San Bernardino", "CA"), ("Tacoma", "WA"), ("Port St. Lucie", "FL"),
        ("Huntsville", "AL"), ("Modesto", "CA"), ("Des Moines", "IA"), ("Fontana", "CA"),
        ("Moreno Valley", "CA"), ("Frisco", "TX"), ("Rochester", "NY"), ("Fayetteville", "NC"),
        ("Yonkers", "NY"), ("Cape Coral", "FL"), ("Worcester", "MA"), ("Columbus", "GA"),
        ("Salt Lake City", "UT"), ("Little Rock", "AR"), ("McKinney", "TX"), ("Augusta", "GA"),
        ("Oxnard", "CA"), ("Amarillo", "TX"), ("Tallahassee", "FL"), ("Birmingham", "AL"),
        ("Grand Prairie", "TX"), ("Montgomery", "AL"), ("Grand Rapids", "MI"), ("Sioux Falls", "SD"),
        ("Overland Park", "KS"), ("Huntington Beach", "CA"), ("Peoria", "AZ"), ("Knoxville", "TN"),
        ("Vancouver", "WA"), ("Glendale", "CA"), ("Providence", "RI"), ("Akron", "OH"),
        ("Brownsville", "TX"), ("Tempe", "AZ"), ("Mobile", "AL"), ("Newport News", "VA"),
        ("Shreveport", "LA"), ("Fort Lauderdale", "FL"), ("Chattanooga", "TN"), ("Aurora", "IL"),
        ("Ontario", "CA"), ("Eugene", "OR"), ("Elk Grove", "CA"), ("Santa Rosa", "CA"),
        ("Cary", "NC"), ("Salem", "OR"), ("Rancho Cucamonga", "CA"), ("Oceanside", "CA"),
        ("Clarksville", "TN"), ("Garden Grove", "CA"), ("Pembroke Pines", "FL"), ("Lancaster", "CA"),
        ("Fort Collins", "CO"), ("Springfield", "MO"), ("Palmdale", "CA"), ("Salinas", "CA"),
        ("Hayward", "CA"), ("Corona", "CA"), ("Paterson", "NJ"), ("Murfreesboro", "TN"),
        ("Alexandria", "VA"), ("Macon", "GA"), ("Lakewood", "CO"), ("Killeen", "TX"),
        ("Kansas City", "KS"), ("Springfield", "MA"), ("Sunnyvale", "CA"), ("Hollywood", "FL"),
        ("Roseville", "CA"), ("Charleston", "SC"), ("Bellevue", "WA"), ("Escondido", "CA"),
        ("Jackson", "MS"), ("Joliet", "IL"), ("Surprise", "AZ"), ("Naperville", "IL"),
        ("Pasadena", "TX"), ("Mesquite", "TX"), ("Pomona", "CA"), ("Bridgeport", "CT"),
        ("Rockford", "IL"), ("Savannah", "GA"), ("Denton", "TX"), ("Syracuse", "NY"),
        ("McAllen", "TX"), ("Olathe", "KS"), ("Gainesville", "FL"), ("Torrance", "CA"),
        ("Thornton", "CO"), ("Visalia", "CA"), ("Waco", "TX"), ("Fullerton", "CA"),
        ("Orange", "CA"), ("Warren", "MI"), ("Columbia", "SC"), ("West Valley City", "UT"),
        ("Hampton", "VA"), ("Cedar Rapids", "IA"), ("Dayton", "OH"), ("Pasadena", "CA"),
        ("Miramar", "FL"), ("Victorville", "CA"), ("Elizabeth", "NJ"), ("Stamford", "CT"),
        ("Kent", "WA"), ("Midland", "TX"), ("Coral Springs", "FL"), ("Sterling Heights", "MI"),
        ("New Haven", "CT"), ("Carrollton", "TX"), ("Santa Clara", "CA"), ("Fargo", "ND"),
        ("Norman", "OK"), ("Lewisville", "TX"), ("Columbia", "MO"), ("Abilene", "TX"),
        ("Athens", "GA"), ("Topeka", "KS"), ("Pearland", "TX"), ("Simi Valley", "CA"),
        ("Thousand Oaks", "CA"), ("Allentown", "PA"), ("Palm Bay", "FL"), ("Meridian", "ID"),
        ("Vallejo", "CA"), ("Round Rock", "TX"), ("Concord", "CA"), ("Arvada", "CO"),
        ("Clovis", "CA"), ("College Station", "TX"), ("Independence", "MO"), ("Rochester", "MN"),
        ("Lafayette", "LA"), ("Ann Arbor", "MI"), ("Berkeley", "CA"), ("Fairfield", "CA"),
        ("Hartford", "CT"), ("West Palm Beach", "FL"), ("Wilmington", "NC"), ("Billings", "MT"),
        ("Richardson", "TX"), ("Cambridge", "MA"), ("North Charleston", "SC"), ("Clearwater", "FL"),
        ("Lakeland", "FL"), ("Evansville", "IN"), ("West Jordan", "UT"), ("Broken Arrow", "OK"),
        ("Antioch", "CA"), ("Westminster", "CO"), ("Manchester", "NH"), ("Richmond", "CA"),
        ("High Point", "NC"), ("League City", "TX"), ("Lowell", "MA"), ("Carlsbad", "CA"),
        ("Waterbury", "CT"), ("Provo", "UT"), ("Elgin", "IL"), ("Odessa", "TX"),
        ("Springfield", "IL"), ("Beaumont", "TX"), ("Gresham", "OR"), ("Las Cruces", "NM"),
        ("Lansing", "MI"), ("Pompano Beach", "FL"), ("Peoria", "IL"), ("Downey", "CA"),
        ("Murrieta", "CA"), ("Pueblo", "CO"), ("Miami Gardens", "FL"), ("Everett", "WA"),
        ("Costa Mesa", "CA"), ("Temecula", "CA"), ("Ventura", "CA"), ("Santa Maria", "CA"),
        ("Sugar Land", "TX"), ("Greeley", "CO"), ("South Fulton", "GA"), ("Sparks", "NV"),
        ("Dearborn", "MI"), ("Tyler", "TX"), ("Tuscaloosa", "AL"), ("Allen", "TX"),
        ("West Covina", "CA"), ("Centennial", "CO"), ("Sandy Springs", "GA"), ("El Monte", "CA"),
        ("Hillsboro", "OR"), ("Menifee", "CA"), ("Green Bay", "WI"), ("Rio Rancho", "NM"),
        ("Concord", "NC"), ("Davie", "FL"), ("Nampa", "ID"), ("Boulder", "CO"),
        ("Jurupa Valley", "CA"), ("Inglewood", "CA"), ("Spokane Valley", "WA"), ("Renton", "WA"),
        ("Burbank", "CA"), ("Brockton", "MA"), ("El Cajon", "CA"), ("Rialto", "CA"),
        ("San Mateo", "CA"), ("Goodyear", "AZ"), ("South Bend", "IN"), ("Lee's Summit", "MO"),
        ("Edinburg", "TX"), ("Daly City", "CA"), ("Wichita Falls", "TX"), ("Vacaville", "CA"),
        ("Chico", "CA"), ("Bend", "OR"), ("Quincy", "MA"), ("Davenport", "IA"),
        ("Fishers", "IN"), ("Lynn", "MA"), ("New Bedford", "MA"), ("Norwalk", "CA"),
        ("Carmel", "IN"), ("Hesperia", "CA"), ("Albany", "NY"), ("Buckeye", "AZ"),
        ("San Angelo", "TX"), ("Federal Way", "WA"), ("St. George", "UT"), ("Kenosha", "WI"),
        ("Longmont", "CO"), ("Boca Raton", "FL"), ("New Braunfels", "TX"), ("Roanoke", "VA"),
        ("Vista", "CA"), ("Yuma", "AZ"), ("Beaverton", "OR"), ("Portsmouth", "VA"),
        ("Fayetteville", "AR"), ("Orem", "UT"), ("Conroe", "TX"), ("Yakima", "WA"),
        ("Suffolk", "VA"), ("Sunrise", "FL"), ("Deltona", "FL"), ("Edmond", "OK"),
        ("Lawrence", "KS"), ("Tracy", "CA"), ("Reading", "PA"), ("Sandy", "UT"),
        ("Asheville", "NC"), ("Palm Coast", "FL"), ("Erie", "PA"), ("San Marcos", "CA"),
        ("Livonia", "MI"), ("Plantation", "FL"), ("Fall River", "MA"), ("Compton", "CA"),
        ("Carson", "CA"), ("Redding", "CA"), ("O'Fallon", "MO"), ("Mount Pleasant", "SC"),
        ("Roswell", "GA"), ("Mission Viejo", "CA"), ("Hoover", "AL"), ("Bellingham", "WA"),
        ("South Gate", "CA"), ("Chino", "CA"), ("Fort Myers", "FL"), ("Kirkland", "WA"),
        ("Santa Monica", "CA"), ("Norwalk", "CT"), ("Nashua", "NH"), ("Indio", "CA"),
        ("Lawton", "OK"), ("Hemet", "CA"), ("Avondale", "AZ"), ("Westminster", "CA"),
        ("Trenton", "NJ"), ("Merced", "CA"), ("Fort Smith", "AR"), ("Clifton", "NJ"),
        ("Waukegan", "IL"), ("Bloomington", "MN"), ("Champaign", "IL"), ("Greenville", "NC"),
        ("San Leandro", "CA"), ("Newton", "MA"), ("Lawrence", "MA"), ("Santa Fe", "NM"),
        ("Santa Barbara", "CA"), ("Springdale", "AR"), ("Troy", "MI"), ("Citrus Heights", "CA"),
        ("Ogden", "UT"), ("Duluth", "MN"), ("Deerfield Beach", "FL"), ("Manteca", "CA"),
        ("Temple", "TX"), ("Mission", "TX"), ("Bryan", "TX"), ("Danbury", "CT"),
        ("Hawthorne", "CA"), ("Whittier", "CA"), ("Livermore", "CA"), ("Lake Forest", "CA"),
        ("Medford", "OR"), ("San Ramon", "CA"), ("Melbourne", "FL"), ("Sioux City", "IA"),
        ("Franklin", "TN"), ("Auburn", "WA"), ("Baytown", "TX"), ("Kennewick", "WA"),
        ("Brooklyn Park", "MN"), ("Newport Beach", "CA"), ("Westland", "MI"), ("Farmington Hills", "MI"),
        ("Cicero", "IL"), ("Buena Park", "CA"), ("Warwick", "RI"), ("Longview", "TX"),
        ("Cranston", "RI"), ("Layton", "UT"), ("Largo", "FL"), ("Redwood City", "CA"),
        ("Mountain View", "CA"), ("Folsom", "CA"), ("Johns Creek", "GA"), ("Lake Charles", "LA"),
        ("Gastonia", "NC"), ("New Rochelle", "NY"), ("Alhambra", "CA"), ("Warner Robins", "GA"),
        ("Miami Beach", "FL"), ("Lehi", "UT"), ("Flint", "MI"), ("Homestead", "FL"),
        ("Rancho Cordova", "CA"), ("Frederick", "MD"), ("Boynton Beach", "FL"), ("Somerville", "MA"),
        ("North Port", "FL"), ("Lakewood", "CA"), ("South Jordan", "UT"), ("Parma", "OH"),
        ("Pharr", "TX"), ("Plymouth", "MN"), ("Kissimmee", "FL"), ("Perris", "CA"),
        ("Lynchburg", "VA"), ("Jonesboro", "AR"), ("Tustin", "CA"), ("Upland", "CA"),
        ("Napa", "CA"), ("Georgetown", "TX"), ("Bloomington", "IN"), ("Auburn", "AL"),
        ("Bloomington", "IL"), ("Pasco", "WA"), ("Milpitas", "CA"), ("Chino Hills", "CA"),
        ("Flower Mound", "TX"), ("Pleasanton", "CA"), ("Cedar Park", "TX"), ("Bellflower", "CA"),
        ("Loveland", "CO"), ("Racine", "WI"), ("Hammond", "IN"), ("Bethlehem", "PA"),
        ("Woodbury", "MN"), ("Alameda", "CA"), ("Wyoming", "MI"), ("Rapid City", "SD"),
        ("Schaumburg", "IL"), ("Castle Rock", "CO"), ("Evanston", "IL"), ("Doral", "FL"),
        ("Flagstaff", "AZ"), ("Arlington Heights", "IL"), ("Rochester Hills", "MI"), ("Scranton", "PA"),
        ("Southfield", "MI"), ("Daytona Beach", "FL"), ("Pittsburg", "CA"), ("Redmond", "WA"),
        ("Missoula", "MT"), ("Apple Valley", "CA"), ("Mansfield", "TX"), ("Pawtucket", "RI"),
        ("Iowa City", "IA"), ("Missouri City", "TX"), ("Broomfield", "CO"), ("Appleton", "WI"),
        ("Rock Hill", "SC"), ("Bismarck", "ND"), ("Lauderhill", "FL"), ("Bolingbrook", "IL")
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
        # Convert "New York" to "new-york"
        city_formatted = city.lower().replace(" ", "-").replace("'", "")
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

    def get_venues_on_page(self) -> List[Dict]:
        """Extract all venues from the current page"""
        venues = []

        try:
            # Wait a moment for page to fully render
            time.sleep(1)

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
                        venue_data = self.extract_venue_data(current_venue_elements[idx])
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
                            venue_data = self.extract_venue_data(current_venue_elements[idx])
                            if venue_data:
                                venues.append(venue_data)
                    except:
                        continue

            print()  # New line after progress

        except Exception as e:
            print(f"  ❌ Error getting venues: {e}")

        return venues

    def click_next_page(self, current_page: int) -> bool:
        """Navigate to the next page using multiple strategies"""
        try:
            # Scroll to bottom first to ensure pagination is visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Get the first venue element for verification
            try:
                first_venue_elem = self.driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
                first_venue_name_elem = first_venue_elem.find_element(By.CSS_SELECTOR, "[class*='vendor-name']")
                first_venue_name = first_venue_name_elem.text.strip()
            except:
                first_venue_elem = None
                first_venue_name = ""

            next_page_num = current_page + 1

            # Strategy 1: Try multiple button selector variations
            button_selectors = [
                f"button[aria-label='Go to page {next_page_num}']",
                f"button[aria-label='Page {next_page_num}']",
                f"button[aria-label='page {next_page_num}']",
                f"button[aria-label*='page {next_page_num}']",
                f"a[aria-label='Go to page {next_page_num}']",
                f"a[aria-label='Page {next_page_num}']",
            ]

            button_found = False
            for selector in button_selectors:
                try:
                    page_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    print(f"  🔍 Found button with selector: {selector}")

                    # Scroll button into view
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", page_button)
                    time.sleep(1)

                    # Click using JavaScript
                    self.driver.execute_script("arguments[0].click();", page_button)
                    print(f"  ⏳ Clicked page {next_page_num} button, waiting for page load...")

                    button_found = True
                    break
                except NoSuchElementException:
                    continue

            if not button_found:
                # Strategy 2: Try finding "Next" button
                next_button_selectors = [
                    "button[aria-label='Go to next page']",
                    "button[aria-label='Next page']",
                    "button[aria-label*='Next']",
                    "a[aria-label='Go to next page']",
                    "a[aria-label*='Next']",
                ]

                for selector in next_button_selectors:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        print(f"  🔍 Found 'Next' button with selector: {selector}")

                        # Scroll into view and click
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_button)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", next_button)
                        print(f"  ⏳ Clicked 'Next' button, waiting for page load...")

                        button_found = True
                        break
                    except NoSuchElementException:
                        continue

            if not button_found:
                # Strategy 3: Try URL-based pagination
                print(f"  🔍 No pagination button found, trying URL-based navigation...")
                current_url = self.driver.current_url

                # Try different URL parameter approaches
                url_params_to_try = [
                    f"&page={next_page_num}",
                    f"?page={next_page_num}",
                    f"&p={next_page_num}",
                    f"&offset={(next_page_num - 1) * 30}",
                ]

                for param in url_params_to_try:
                    try:
                        # Check if URL already has query params
                        if '?' in current_url:
                            new_url = current_url.split('&page=')[0].split('&p=')[0].split('&offset=')[0] + param.replace('?', '&')
                        else:
                            new_url = current_url + param

                        print(f"  ⏳ Trying URL: {new_url[:100]}...")
                        self.driver.get(new_url)
                        button_found = True
                        break
                    except:
                        continue

            if not button_found:
                print(f"  ℹ️  No pagination method worked - assuming last page")
                return False

            # Wait for page to load and verify content changed
            time.sleep(3)

            # Wait for venues to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "section[data-testid='vendor-card-base']"))
                )
            except TimeoutException:
                print(f"  ⚠️  Timeout waiting for venues after navigation")
                return False

            # Verify the page actually changed by checking first venue
            if first_venue_name:
                try:
                    time.sleep(2)  # Extra wait for content to stabilize
                    new_first_venue_elem = self.driver.find_element(By.CSS_SELECTOR, "section[data-testid='vendor-card-base']")
                    new_first_venue_name_elem = new_first_venue_elem.find_element(By.CSS_SELECTOR, "[class*='vendor-name']")
                    new_first_venue_name = new_first_venue_name_elem.text.strip()

                    if new_first_venue_name and new_first_venue_name != first_venue_name:
                        print(f"  ✅ Page changed! ('{first_venue_name[:30]}...' → '{new_first_venue_name[:30]}...')")
                        return True
                    else:
                        print(f"  ⚠️  First venue unchanged ('{first_venue_name[:30]}...') - may be last page")
                        return False
                except Exception as e:
                    print(f"  ⚠️  Could not verify page change: {e}")
                    # If we can't verify but found venues, assume success
                    return True

            # If no first venue to compare, assume success if venues are present
            return True

        except Exception as e:
            print(f"  ⚠️  Error navigating to next page: {e}")
            return False

    def scrape_city(self, city: str, state: str) -> List[Dict]:
        """Scrape all venues for a given city"""
        print(f"\n🔍 Scraping {city}, {state}...")

        url = self.format_city_url(city, state)
        city_venues = []
        seen_venues = set()  # Track name+location to detect duplicates
        page_num = 1
        consecutive_duplicate_pages = 0  # Count pages with all duplicates

        try:
            self.driver.get(url)

            if not self.wait_for_page_load():
                print(f"  ⚠️  No venues found for {city}, {state}")
                return city_venues

            while True:
                print(f"  📄 Processing page {page_num}...")

                # Get venues from current page
                venues = self.get_venues_on_page()

                # Add all venues without duplicate checking (user will handle in post-processing)
                for venue in venues:
                    venue['search_city'] = city
                    venue['search_state'] = state
                    city_venues.append(venue)

                print(f"  ✅ Extracted {len(venues)} venues from page {page_num}")

                # Try to go to next page
                if not self.click_next_page(page_num):
                    print(f"  ✅ Reached last page")
                    break

                page_num += 1

                # Safety limit to prevent infinite loops
                if page_num > 50:
                    print(f"  ⚠️  Reached page limit (50)")
                    break

            print(f"✅ Total venues found for {city}, {state}: {len(city_venues)}")

        except Exception as e:
            print(f"❌ Error scraping {city}, {state}: {e}")

        return city_venues

    def scrape_all_cities(self, start_index: int = 0, limit: Optional[int] = None):
        """Scrape venues for all cities in the list"""
        print(f"🚀 Starting scrape for {len(self.CITIES)} cities...")
        print(f"⏰ This may take several hours to complete")

        cities_to_scrape = self.CITIES[start_index:start_index + limit] if limit else self.CITIES[start_index:]

        for idx, (city, state) in enumerate(cities_to_scrape, start=start_index + 1):
            print(f"\n{'='*60}")
            print(f"Progress: {idx}/{len(self.CITIES)} cities")
            print(f"{'='*60}")

            city_venues = self.scrape_city(city, state)
            self.all_venues.extend(city_venues)

            # Rate limiting: wait between cities
            if idx < len(self.CITIES):
                wait_time = 3
                print(f"⏳ Waiting {wait_time} seconds before next city...")
                time.sleep(wait_time)

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
    print("=" * 60)
    print("The Knot Wedding Venue Scraper")
    print("=" * 60)

    scraper = TheKnotVenueScraper(headless=True)

    try:
        scraper.setup_driver()

        # For testing, you can limit the number of cities:
        # scraper.scrape_all_cities(start_index=0, limit=3)

        # To scrape all cities:
        scraper.scrape_all_cities()

        # Export results
        scraper.export_to_csv("wedding_venues_outdoor_data.csv")

    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print(f"💾 Saving {len(scraper.all_venues)} venues collected so far...")
        scraper.export_to_csv("wedding_venues_outdoor_data_partial.csv")

    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")

    finally:
        scraper.close()


if __name__ == "__main__":
    main()

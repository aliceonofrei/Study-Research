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

    def click_next_page(self) -> bool:
        """Click the next page button if available"""
        try:
            # Scroll to bottom first to ensure pagination is visible
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Get current page number and URL before clicking
            current_url = self.driver.current_url
            try:
                current_page_elem = self.driver.find_element(By.CSS_SELECTOR, "button[aria-current='page']")
                current_page_text = current_page_elem.text
                current_page = int(current_page_text)
                print(f"  📍 Currently on page {current_page}")
            except Exception as e:
                print(f"  ⚠️  Could not detect current page number: {e}")
                current_page = None

            # Check if "Go to next page" link exists
            try:
                next_link = self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='Go to next page']")
                print(f"  🔍 Found next button, clicking...")

                # Click using JavaScript
                self.driver.execute_script("arguments[0].click();", next_link)

                # Wait for page to load
                time.sleep(4)

                # Verify page actually changed
                new_url = self.driver.current_url
                if current_url == new_url:
                    print(f"  ⚠️  URL didn't change - pagination may not be working")

                # Check new page number
                if current_page:
                    try:
                        new_page_elem = self.driver.find_element(By.CSS_SELECTOR, "button[aria-current='page']")
                        new_page_text = new_page_elem.text
                        new_page = int(new_page_text)

                        if new_page == current_page:
                            print(f"  ⚠️  Page number didn't change (still on {current_page}) - reached last page")
                            return False

                        print(f"  ✅ Advanced from page {current_page} to page {new_page}")
                    except Exception as e:
                        print(f"  ⚠️  Could not verify new page number: {e}")

                return True

            except NoSuchElementException:
                print(f"  ℹ️  No next page button found - reached last page")
                return False

        except Exception as e:
            print(f"  ⚠️  Error clicking next page: {e}")
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

                # Check for duplicate venues (indicates we're looping)
                # Use name+location as unique identifier
                new_venues_count = 0
                for venue in venues:
                    venue_name = venue.get('name', '')
                    venue_location = venue.get('location', '')
                    venue_key = (venue_name, venue_location)

                    if venue_key not in seen_venues:
                        seen_venues.add(venue_key)
                        venue['search_city'] = city
                        venue['search_state'] = state
                        city_venues.append(venue)
                        new_venues_count += 1

                if new_venues_count == 0 and len(venues) > 0:
                    consecutive_duplicate_pages += 1
                    print(f"  ⚠️  All {len(venues)} venues on this page are duplicates (duplicate page #{consecutive_duplicate_pages})")

                    if consecutive_duplicate_pages >= 2:
                        print(f"  ⚠️  Two consecutive pages of duplicates - reached end of results")
                        break
                else:
                    consecutive_duplicate_pages = 0
                    print(f"  ✅ Extracted {new_venues_count} new venues from page {page_num}")

                # Try to go to next page
                if not self.click_next_page():
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

#!/usr/bin/env python3
"""
Wedding Venue Scraper - Missing Cities Only

This script scrapes ONLY the cities that were missed due to formatting issues.
It will append data to both existing CSV files.

Author: AI-Assisted
Date: 2026-01-26
"""

from wedding_venue_scraper import TheKnotVenueScraper


# Only the 14 cities that were missed due to formatting issues
MISSING_CITIES = [
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


def scrape_missing_for_regular():
    """Scrape missing cities for regular outdoor venues (no price filter)"""
    print("\n" + "=" * 60)
    print("🔧 SCRAPING MISSING CITIES - REGULAR OUTDOOR VENUES")
    print("=" * 60)
    print(f"📋 {len(MISSING_CITIES)} cities to scrape")
    print("💾 Output: wedding_venues_outdoor_data.csv")
    print("=" * 60)

    scraper = TheKnotVenueScraper(headless=True)

    # Override the city list with only missing cities
    scraper.CITIES = MISSING_CITIES

    try:
        scraper.setup_driver()
        scraper.scrape_all_cities(
            start_index=0,
            output_file="wedding_venues_outdoor_data.csv"
        )
        print(f"\n✅ Regular venues: Added {len(scraper.all_venues)} venues for missing cities")
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print(f"💾 Data already saved via auto-save")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
    finally:
        scraper.close()


def scrape_missing_for_affordable():
    """Scrape missing cities for affordable outdoor venues"""
    print("\n" + "=" * 60)
    print("🔧 SCRAPING MISSING CITIES - AFFORDABLE OUTDOOR VENUES")
    print("=" * 60)
    print(f"📋 {len(MISSING_CITIES)} cities to scrape")
    print("💾 Output: wedding_venues_outdoor_affordable_data.csv")
    print("=" * 60)

    scraper = TheKnotVenueScraper(headless=True)

    # Override the city list with only missing cities
    scraper.CITIES = MISSING_CITIES

    # Override BASE_URL to include price_range=affordable
    scraper.BASE_URL = "https://www.theknot.com/marketplace/wedding-reception-venues-{}-{}?price_range=affordable&venue-amenities=uncovered-outdoor-wedding-reception-site+covered-outdoor-wedding-reception-site&sort=recommended"

    try:
        scraper.setup_driver()
        scraper.scrape_all_cities(
            start_index=0,
            output_file="wedding_venues_outdoor_affordable_data.csv"
        )
        print(f"\n✅ Affordable venues: Added {len(scraper.all_venues)} venues for missing cities")
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user")
        print(f"💾 Data already saved via auto-save")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
    finally:
        scraper.close()


def main():
    """Main function - scrape missing cities for both datasets"""
    print("\n" + "🔧" * 30)
    print("SCRAPING 14 MISSING CITIES ONLY")
    print("🔧" * 30)

    print("\nMissing cities due to formatting issues:")
    for city, state in MISSING_CITIES:
        print(f"  - {city}, {state}")

    print("\nThis will scrape these cities and add them to your existing CSVs.")
    print("=" * 60)

    # Scrape for regular outdoor venues
    scrape_missing_for_regular()

    print("\n" + "=" * 60)
    input("\nPress Enter to continue to affordable venues scraping...")

    # Scrape for affordable outdoor venues
    scrape_missing_for_affordable()

    print("\n" + "=" * 60)
    print("✅ COMPLETE! Missing cities have been added to both CSV files.")
    print("=" * 60)


if __name__ == "__main__":
    main()

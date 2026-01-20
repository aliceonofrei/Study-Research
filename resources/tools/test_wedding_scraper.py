#!/usr/bin/env python3
"""
Test Script for Wedding Venue Scraper

This script tests the scraper with a single city to verify it's working correctly
before running the full scrape of all 489 cities.

Author: AI-Assisted
Date: 2026-01-20
"""

from wedding_venue_scraper import TheKnotVenueScraper


def test_single_city():
    """Test scraper with Seattle, WA"""
    print("=" * 60)
    print("Testing Wedding Venue Scraper")
    print("=" * 60)
    print("\n🧪 This will test the scraper with Seattle, WA")
    print("📊 Expected: Multiple pages of outdoor wedding venues\n")

    scraper = TheKnotVenueScraper(headless=False)  # Show browser for testing

    try:
        print("🚀 Setting up browser...")
        scraper.setup_driver()

        print("✅ Browser ready\n")

        # Test with Seattle, WA
        venues = scraper.scrape_city("Seattle", "WA")

        print("\n" + "=" * 60)
        print("Test Results")
        print("=" * 60)
        print(f"✅ Venues found: {len(venues)}")

        if venues:
            print("\n📋 Sample venue data (first 3):")
            for i, venue in enumerate(venues[:3], 1):
                print(f"\n{i}. {venue['name']}")
                print(f"   Location: {venue['location']}")
                print(f"   City/Area: {venue['city_area']}")
                print(f"   Rating: {venue['rating']}")
                print(f"   Reviews: {venue['num_reviews']}")

            # Export test data
            scraper.all_venues = venues
            scraper.export_to_csv("test_wedding_venues.csv")

            print("\n✅ Test successful!")
            print("💡 Review test_wedding_venues.csv to verify data format")
            print("💡 If data looks good, run the full scraper: python wedding_venue_scraper.py")
        else:
            print("\n⚠️  No venues found - this might indicate an issue")
            print("💡 Check if:")
            print("   - The website is accessible")
            print("   - CSS selectors need updating")
            print("   - Your internet connection is stable")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("💡 Check the error message and README for troubleshooting")

    finally:
        print("\n🔄 Closing browser...")
        scraper.close()


def test_url_formatting():
    """Test URL formatting for various cities"""
    print("\n" + "=" * 60)
    print("Testing URL Formatting")
    print("=" * 60)

    scraper = TheKnotVenueScraper()

    test_cities = [
        ("New York", "NY"),
        ("Los Angeles", "CA"),
        ("St. Louis", "MO"),
        ("O'Fallon", "MO"),
    ]

    for city, state in test_cities:
        url = scraper.format_city_url(city, state)
        print(f"\n{city}, {state}")
        print(f"  → {url}")


def main():
    """Main test function"""
    print("\n🧪 Wedding Venue Scraper Test Suite\n")

    # Test URL formatting first
    test_url_formatting()

    print("\n" + "=" * 60)
    input("\n⏸️  Press Enter to start browser test with Seattle, WA...")

    # Test actual scraping
    test_single_city()


if __name__ == "__main__":
    main()

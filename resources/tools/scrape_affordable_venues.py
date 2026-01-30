#!/usr/bin/env python3
"""
Wedding Venue Scraper - Affordable Outdoor Venues

This script scrapes AFFORDABLE outdoor wedding venues from TheKnot.com
for 500 US cities and saves to a separate CSV file.

Author: AI-Assisted
Date: 2026-01-26
"""

from wedding_venue_scraper import TheKnotVenueScraper


def main():
    """Main function to run the affordable venue scraper"""
    print("\n" + "=" * 60)
    print("🏞️  THE KNOT - AFFORDABLE OUTDOOR WEDDING VENUE SCRAPER")
    print("=" * 60)
    print("📋 Scraping affordable outdoor venues (covered + uncovered)")
    print("💾 Output: wedding_venues_outdoor_affordable_data.csv")
    print("=" * 60)

    # Initialize scraper with 'affordable' price range
    scraper = TheKnotVenueScraper(headless=True, price_range='affordable')

    try:
        scraper.setup_driver()

        # Scrape all 500 cities
        # The output file is specified here
        scraper.scrape_all_cities(
            start_index=0,
            output_file="wedding_venues_outdoor_affordable_data.csv"
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

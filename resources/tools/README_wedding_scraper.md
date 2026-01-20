# Wedding Venue Scraper for The Knot

> **Date Created:** 2026-01-20
> **Purpose:** Scrape outdoor wedding venue data from TheKnot.com for analysis
> **Status:** Ready for use

## Overview

This Python script scrapes wedding venue data from TheKnot.com, specifically targeting outdoor wedding venues (both covered and uncovered) across 500 US cities. The script automatically handles pagination and exports data to CSV format.

## Features

- ✅ Scrapes all pages for each city (automatic pagination)
- ✅ Collects venue name, location, rating, and number of reviews
- ✅ Extracts city/area information from location data
- ✅ Handles JavaScript-rendered content using Selenium
- ✅ Includes rate limiting to avoid being blocked
- ✅ Error handling and recovery
- ✅ Progress tracking with detailed console output
- ✅ CSV export with all collected data
- ✅ Keyboard interrupt handling (Ctrl+C saves partial data)

## Data Collected

For each venue, the script collects:

1. **Search City** - The city that was queried
2. **Search State** - The state abbreviation
3. **Venue Name** - Name of the wedding venue
4. **Location** - Full location string from the website
5. **City/Area** - Extracted city or area name
6. **Rating** - Venue rating (e.g., 4.9)
7. **Number of Reviews** - Total review count

## Prerequisites

### 1. Python Installation

Ensure you have Python 3.8 or higher installed:

```bash
python --version
# or
python3 --version
```

### 2. Chrome Browser

The script uses Chrome WebDriver, so you need Google Chrome installed.

### 3. ChromeDriver

Selenium 4.15+ includes Chrome WebDriver Manager, which automatically downloads the appropriate ChromeDriver version. No manual installation needed!

## Installation

### Step 1: Clone or navigate to the repository

```bash
cd /home/user/Study-Research/resources/tools
```

### Step 2: Install Python dependencies

```bash
pip install -r requirements_wedding_scraper.txt
```

Or install directly:

```bash
pip install selenium>=4.15.0
```

### Step 3: Verify installation

```bash
python -c "import selenium; print(selenium.__version__)"
```

## Usage

### Basic Usage (All Cities)

To scrape all 500 cities:

```bash
python wedding_venue_scraper.py
```

**Expected Duration:** Several hours (3-6 hours depending on your internet speed and number of venues)

### Testing with Limited Cities

To test with just the first 3 cities, edit the `main()` function:

```python
# Change this line in main():
scraper.scrape_all_cities(start_index=0, limit=3)
```

Then run:

```bash
python wedding_venue_scraper.py
```

### Starting from a Specific City

If the scraper was interrupted, you can resume from a specific city index:

```python
# Start from the 50th city:
scraper.scrape_all_cities(start_index=49)
```

### Headless vs. Visible Browser

By default, the script runs in headless mode (no browser window). To see the browser:

```python
# In main():
scraper = TheKnotVenueScraper(headless=False)
```

## Output

### Console Output

The script provides detailed progress information:

```
============================================================
The Knot Wedding Venue Scraper
============================================================
🚀 Starting scrape for 500 cities...
⏰ This may take several hours to complete

============================================================
Progress: 1/500 cities
============================================================

🔍 Scraping New York, NY...
  📄 Processing page 1...
  Found 30 venue cards on page
  ✅ Extracted 30 venues from page 1
  📄 Processing page 2...
  ...
✅ Total venues found for New York, NY: 120
⏳ Waiting 3 seconds before next city...
```

### CSV Output

Data is exported to `wedding_venues_outdoor_data.csv` with the following columns:

| search_city | search_state | name | location | city_area | rating | num_reviews |
|-------------|--------------|------|----------|-----------|--------|-------------|
| Seattle | WA | Beautiful Garden Estate | Seattle, WA | Seattle | 4.9 | 156 |
| Seattle | WA | Mountain View Lodge | Snoqualmie, WA | Snoqualmie | 4.8 | 89 |

### Partial Data (Interrupted Scraping)

If you interrupt the script (Ctrl+C), it automatically saves partial data to:
`wedding_venues_outdoor_data_partial.csv`

## Cities Included

The script scrapes **500 US cities**, including:

- All top 50 US cities by population
- Major metropolitan areas
- Cities across all 50 states
- From New York, NY to Bolingbrook, IL

See the `CITIES` list in the script for the complete list.

## Configuration

### Rate Limiting

The script waits 3 seconds between cities by default. To adjust:

```python
# In scrape_all_cities() method, change:
wait_time = 3  # Change to desired seconds
```

### Timeout Settings

To adjust page load timeout:

```python
# In wait_for_page_load() method:
def wait_for_page_load(self, timeout: int = 15):  # Change default timeout
```

### Page Limit

To prevent infinite loops, the script has a 50-page limit per city. To adjust:

```python
# In scrape_city() method:
if page_num > 50:  # Change limit
```

## Troubleshooting

### Issue: "ChromeDriver not found"

**Solution:** Update Selenium to version 4.15+:
```bash
pip install --upgrade selenium
```

### Issue: "Timeout waiting for venues to load"

**Possible causes:**
- Slow internet connection
- The Knot website is down or blocking requests
- No venues available for that city

**Solution:**
- Increase timeout in `wait_for_page_load(timeout=30)`
- Check if the website is accessible in your browser

### Issue: Script crashes frequently

**Solution:**
- Run with visible browser to see what's happening: `headless=False`
- Check your internet connection
- Increase wait times between requests

### Issue: Empty or incomplete data

**Possible causes:**
- Website HTML structure has changed
- Venue cards have different data attributes

**Solution:**
- Inspect the website's HTML using browser DevTools
- Update the CSS selectors in `extract_venue_data()` method
- Look for `data-testid` attributes that may have changed

### Issue: Getting blocked by the website

**Solution:**
- Increase wait times between cities (currently 3 seconds)
- Add random delays: `time.sleep(random.uniform(3, 7))`
- Use rotating user agents
- Consider using proxies

## Customization

### Changing Filters

The script currently filters for:
- Uncovered outdoor wedding reception sites
- Covered outdoor wedding reception sites

To modify filters, update the `BASE_URL` in the `TheKnotVenueScraper` class:

```python
BASE_URL = "https://www.theknot.com/marketplace/wedding-reception-venues-{}-{}?venue-amenities=YOUR-FILTERS-HERE&sort=recommended"
```

### Adding More Cities

Add cities to the `CITIES` list:

```python
CITIES = [
    # Existing cities...
    ("Your City", "ST"),
]
```

### Extracting Additional Data

To extract more venue information, modify the `extract_venue_data()` method:

```python
# Add new fields:
try:
    price_element = venue_element.find_element(By.CSS_SELECTOR, "[data-testid='vendor-price']")
    venue_data['price_range'] = price_element.text.strip()
except NoSuchElementException:
    pass
```

## Performance Optimization

### For Faster Scraping

1. **Reduce wait times** (but risk being blocked):
   ```python
   wait_time = 1  # Reduce from 3 to 1 second
   ```

2. **Run multiple instances** for different city ranges:
   ```bash
   # Terminal 1: Cities 0-100
   python wedding_venue_scraper.py  # Edit to use start_index=0, limit=100

   # Terminal 2: Cities 100-200
   python wedding_venue_scraper.py  # Edit to use start_index=100, limit=100
   ```

3. **Use headless mode** (default):
   ```python
   scraper = TheKnotVenueScraper(headless=True)
   ```

## Data Analysis

After scraping, you can analyze the data using pandas:

```python
import pandas as pd

# Load data
df = pd.read_csv('wedding_venues_outdoor_data.csv')

# Summary statistics
print(f"Total venues: {len(df)}")
print(f"Cities with data: {df['search_city'].nunique()}")
print(f"Average rating: {df['rating'].astype(float).mean():.2f}")

# Top cities by venue count
top_cities = df['search_city'].value_counts().head(10)
print("\nTop 10 cities by outdoor venue count:")
print(top_cities)

# Rating distribution
print("\nRating distribution:")
print(df['rating'].value_counts().sort_index())
```

## Legal and Ethical Considerations

⚠️ **Important:**

- This script is for **educational and research purposes only**
- Review The Knot's Terms of Service before scraping
- Respect robots.txt directives
- Use reasonable rate limiting to avoid overwhelming the server
- Do not use scraped data for commercial purposes without permission
- Consider reaching out to The Knot for official API access if available

## Support and Contributions

For issues or improvements:

1. Check the troubleshooting section above
2. Review The Knot website for HTML structure changes
3. Update CSS selectors as needed
4. Consider submitting improvements to the repository

## Version History

- **v1.0** (2026-01-20): Initial release
  - Support for 500 US cities
  - Automatic pagination
  - CSV export
  - Error handling and recovery

## License

This script is provided as-is for educational purposes. Use responsibly and in accordance with The Knot's Terms of Service.

---

**Last Updated:** 2026-01-20
**Maintained by:** AI-Assisted Development

# Wedding Venue Scraper Usage Guide

## Overview

Two separate scrapers for The Knot wedding venue data:

1. **`wedding_venue_scraper.py`** - All outdoor venues (no price filter)
2. **`scrape_affordable_venues.py`** - Affordable outdoor venues only

Both scrapers:
- Target the same 500 US cities
- Scrape covered + uncovered outdoor venues
- Auto-save after every city (data loss protection)
- Resume from existing CSV automatically
- Can be safely stopped with Ctrl+C

## Quick Start

### Scrape All Outdoor Venues

```bash
cd "D:\Study Research GitHub\Study-Research\resources\tools"
python wedding_venue_scraper.py
```

Output: `wedding_venues_outdoor_data.csv`

### Scrape Affordable Outdoor Venues

```bash
cd "D:\Study Research GitHub\Study-Research\resources\tools"
python scrape_affordable_venues.py
```

Output: `wedding_venues_outdoor_affordable_data.csv`

## Features

### Auto-Save Protection
- Data saved after **every city** completes
- Maximum data loss: 1 city (not entire session)
- Safe to stop anytime with **Ctrl+C**

### Resume Capability
- Automatically loads existing CSV on startup
- Skips already-scraped cities
- Continues from where you left off

### Error Handling
- Retry logic for timeouts (3 attempts per city)
- Browser crash recovery with restart
- Exponential backoff for network issues
- Stale element handling during pagination

## Output Files

### All Outdoor Venues
- **File**: `wedding_venues_outdoor_data.csv`
- **URL**: No price filter
- **Example**: https://www.theknot.com/marketplace/wedding-reception-venues-seattle-wa?venue-amenities=uncovered-outdoor-wedding-reception-site+covered-outdoor-wedding-reception-site&sort=recommended

### Affordable Outdoor Venues
- **File**: `wedding_venues_outdoor_affordable_data.csv`
- **URL**: `price_range=affordable` filter
- **Example**: https://www.theknot.com/marketplace/wedding-reception-venues-seattle-wa?price_range=affordable&venue-amenities=uncovered-outdoor-wedding-reception-site+covered-outdoor-wedding-reception-site&sort=recommended

## CSV Format

Both files have the same structure:

```
search_city,search_state,name,location,city_area,rating,num_reviews
Seattle,WA,Venue Name,Full Address,City Area,4.9,123
```

## What You'll See

### On Startup

```
🚀 Starting scrape for 500 cities...
💾 Auto-save enabled: Data saved after every city to [filename].csv
✅ Loaded 1250 existing venues from [filename].csv
✅ Already scraped 145 cities
⏭️  Skipping New York, NY (already scraped)
⏭️  Skipping Los Angeles, CA (already scraped)
...
```

### After Each City

```
🚀 Scraping Ann Arbor, MI...
✅ Extracted 30 venues from page 1
✅ Extracted 28 venues from page 2
✅ Total venues for Ann Arbor, MI: 58 (56 new, 2 duplicates)
📈 Total venues collected so far: 1306
💾 Auto-saving to [filename].csv...
✅ Saved! Safe to stop anytime with Ctrl+C
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'selenium'"

Install selenium:
```bash
pip install selenium
```

### Scraper starts from beginning instead of resuming

Make sure you pulled the latest code:
```bash
cd "D:\Study Research GitHub\Study-Research"
git pull origin claude/wedding-venue-scraper-zXW16
```

Check if `import os` is in the imports (line 22).

### CSV file not updating

- Verify auto-save messages appear after each city
- Check file last modified time in Windows Explorer
- Ensure CSV is NOT open in Excel while scraping
- Look for error messages like "⚠️ Auto-save failed"

### Power outage recovery

The scraper will automatically:
1. Load your existing CSV
2. Skip all completed cities
3. Resume from the next city

You'll only lose the city that was being scraped when power went out.

## Running Both Scrapers

You can run both scrapers simultaneously (different terminal windows) or sequentially. They use **different output files** so there's no conflict.

**Recommended**: Run sequentially to avoid overloading your system/network.

## Estimated Time

- **Per city**: 30 seconds to 5 minutes (depends on number of pages)
- **500 cities**: 4-40 hours total
- **Auto-save**: Adds ~1 second per city (negligible)

## Need Help?

Check for errors in the terminal output. Common issues:
- Network timeouts (handled automatically with retries)
- Browser crashes (handled automatically with restart)
- Permission denied (close CSV file in Excel)

---

Last Updated: 2026-01-26

# Estonia Olympics Tracker - Technical Documentation

**Live Site**: https://emoggio.github.io/EstonianMedalist-/
**Repository**: https://github.com/emoggio/EstonianMedalist-
**Local Path**: `C:\Users\eu.moggio\Desktop\Olympics`

## Project Overview

A mobile-friendly website tracking Estonia's performance at Milano Cortina 2026 Winter Olympics with:
- Real-time medal counter
- Estonian flag colors theme (blue, black, white)
- Continuous snowfall effect when medals are won
- Growing snow pile at bottom of viewport
- Automated medal count updates every 3 hours
- Competition schedules with dates/times

## File Structure

```
Olympics/
├── index.html              # Main webpage
├── styles.css              # Estonian-themed styling + snowfall effects
├── script.js               # Data loading + snowfall logic
├── data.json              # Olympic data (medals, athletes, schedules)
├── scraper.py             # Python scraper for auto-updates
├── requirements.txt       # Python dependencies
├── .github/workflows/
│   └── update-results.yml # GitHub Actions workflow (runs every 3 hours)
├── README.md              # User documentation
├── SETUP.md               # Deployment guide
└── PROJECT.md             # This file (technical documentation)
```

## Key Features

### 1. Main Question Display
- Shows "Has Estonia won any medals yet?"
- Answer: "No" (blue border) or "Yes" (gold gradient, pulsing, glowing)
- Changes automatically based on `data.json` medal count

### 2. Medal Counter
- Displays 🥇 🥈 🥉 with counts
- Blue-to-black gradient background (Estonian colors)
- Auto-updates from scraper every 3 hours

### 3. Athlete Lists

#### Completed Events
- Shows athletes who finished competing
- Displays result (e.g., "8th place (2 wins, 4 losses)")
- Shows medal emoji if they won
- Medal winners get special card styling (gold/silver/bronze gradient)

#### Upcoming Events
- Shows athletes yet to compete
- Displays date/time (e.g., "📅 Feb 12, 2026 - 2:15 PM CET")
- Uses real Olympic schedule dates

### 4. Snowfall Effect

**Triggers:**
- When `medals.gold + medals.silver + medals.bronze > 0`
- OR on February 22, 2026 (last day of Olympics) regardless of medal count

**Behavior:**
- Initial burst: 50 snowflakes over 3 seconds
- Continuous: 1 snowflake every 200ms
- Random snowflake symbols: ❄ ❅ ❆
- Random sizes (0.5rem to 1.5rem)
- Random fall durations (4-7 seconds)
- Rotation during fall

**Snow Pile:**
- Fixed to bottom of viewport (not page bottom)
- Grows 0.3px per snowflake
- Max height: 120px
- Rounded top with snowflake decorations
- Glowing white effect
- Melts away if medals go to 0

### 5. Estonian Flag
- Fixed position top-right corner
- Three horizontal stripes (blue, black, white)
- Hover effect: scales to 1.1x

### 6. Color Scheme
- **Estonian blue**: `#0072CE` (flag color)
- **Estonian black**: `#000000` (flag color)
- **Estonian white**: `#FFFFFF` (flag color)
- Background: Gradient from Estonian blue → light blue → ice white
- Text gradients use Estonian colors
- Maintains Milano Cortina 2026 visual style (curves, flowing lines)

## Data Structure (data.json)

```json
{
  "medals": {
    "gold": 0,
    "silver": 0,
    "bronze": 0
  },
  "completed": [
    {
      "name": "Athlete Name",
      "sport": "Sport Name - Event",
      "result": "Placement or outcome",
      "medal": "gold|silver|bronze"  // Optional, only if they won
    }
  ],
  "upcoming": [
    {
      "name": "Athlete Name",
      "sport": "Sport Name - Event",
      "datetime": "Feb DD, 2026 - HH:MM AM/PM CET"
    }
  ]
}
```

## Automated Updates

### What Auto-Updates
✅ **Medal counts** - Scraped every 3 hours from Olympics.com

### What Requires Manual Updates
📝 **Athlete data**:
- Moving athletes from "upcoming" to "completed"
- Adding competition results
- Updating schedules (if needed)

### GitHub Actions Workflow
- **Schedule**: Runs every 3 hours via cron: `0 */3 * * *`
- **Manual trigger**: Available via Actions tab
- **Process**:
  1. Runs `scraper.py`
  2. Fetches medal counts from Olympics.com
  3. Preserves manually curated athlete data
  4. Commits changes if medals updated
  5. GitHub Pages auto-deploys (1-2 minutes)

### Scraper Behavior
- **URL**: `https://www.olympics.com/en/milano-cortina-2026/medals/est`
- **Strategy**: Multiple parsing strategies (table cells, specific elements, table structure)
- **Reliability**: Medal counts are stable; athlete data is JavaScript-rendered (unreliable to scrape)
- **Fallback**: If scraping fails, preserves existing data

## How to Update Data Manually

### Option 1: On GitHub (Easiest)
1. Go to: https://github.com/emoggio/EstonianMedalist-/edit/main/data.json
2. Edit the JSON (move athletes, add results)
3. Click "Commit changes"
4. Site updates in 1-2 minutes

### Option 2: Locally
```bash
cd C:\Users\eu.moggio\Desktop\Olympics
# Edit data.json
git add data.json
git commit -m "Update results for [athlete name]"
git push origin main
```

### Example: Moving Athlete to Completed
```json
// Move from "upcoming" to "completed"
{
  "name": "Kelly Sildaru",
  "sport": "Freestyle Skiing - Women's Halfpipe",
  "datetime": "Feb 19, 2026 - 6:30 PM CET",  // Keep for reference
  "result": "5th place",
  "medal": "bronze"  // Optional, only if they won
}
```

## Local Testing

### Start Local Server
```bash
cd C:\Users\eu.moggio\Desktop\Olympics
python -m http.server 8000
```

Then open: http://localhost:8000

**Why not `file://`?** CORS security prevents JavaScript from fetching `data.json` directly from filesystem.

### Test Snowflakes Locally
1. Edit `data.json` locally
2. Change `"gold": 1` (or any medal count > 0)
3. Refresh browser at http://localhost:8000
4. See snowflakes fall!
5. **Important**: Revert `data.json` before committing

### Stop Local Server
```bash
# Kill Python server
taskkill /F /IM python.exe
# Or Ctrl+C in the terminal
```

## Estonian Athlete Data (32 athletes, 11 sports)

### Curling (2) - COMPLETED
- Marie Kaldvee & Harri Lill - Mixed Doubles (8th place, 2-4 record)

### Biathlon (8) - Anterselva Arena
- Women: Johanna Talihärm, Regina Ermits, Susan Kuelm, Tuuli Tomingas
- Men: Jakob Kulbin, Kristo Siimer, Mark-Markos Kehva, Rene Zahkna
- Events: Feb 8-21, 2026

### Alpine Skiing (2)
- Women: Hanna Gret Teder
- Men: Tormis Laine

### Freestyle Skiing (3)
- Women: Kelly Sildaru, Grete-Mia Meentalo
- Men: Henry Sildaru

### Cross-Country Skiing (8) - Val di Fiemme
- Women: Kaidy Kaasiku, Keidy Kaasiku, Mariel Merlii Pulles, Teesi Tuul, Teiloora Ojaste
- Men: Alvar Johannes Alev, Karl Sebastian Dremljuga, Martin Himma
- Events: Feb 7-22, 2026

## GitHub Pages Setup

### Enabled Settings
1. **Source**: Branch `main`, folder `/` (root)
2. **Actions Permissions**: Read and write permissions
3. **Allow Actions to create PRs**: Enabled

### Deployment
- Auto-deploys on every push to `main`
- Takes 1-2 minutes to rebuild
- Live at: https://emoggio.github.io/EstonianMedalist-/

## Known Limitations

1. **Athlete data not auto-scraped**
   - Olympics.com uses JavaScript rendering
   - Reliable scraping requires headless browser (Selenium/Playwright)
   - Manual updates are simpler and more reliable

2. **Medal scraping may break**
   - If Olympics.com changes HTML structure
   - Scraper has multiple fallback strategies
   - Will preserve existing data if scraping fails

3. **Snowflakes on mobile**
   - May be performance-intensive on older devices
   - Consider reducing snowflake frequency if needed

4. **Time zone**
   - All times shown in CET (Central European Time)
   - No automatic conversion to user's timezone

## Technical Details

### Snowflake Animation
- CSS animation: `fall` (translateY + rotate)
- JavaScript: Creates DOM elements dynamically
- Each snowflake auto-removes after animation completes
- Z-index: 9999 (above all content)

### Snow Pile
- CSS: Fixed position, gradient background
- JavaScript: Updates height dynamically
- Grows: 0.3px per snowflake
- Melts: 2px per 50ms when medals = 0

### Date Check for Last Day
```javascript
function isLastDayOfOlympics() {
    const now = new Date();
    const lastDay = new Date('2026-02-22');
    return now.getFullYear() === lastDay.getFullYear() &&
           now.getMonth() === lastDay.getMonth() &&
           now.getDate() === lastDay.getDate();
}
```

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile-friendly (responsive design)
- Uses CSS gradients, transforms, animations
- No external dependencies (vanilla JS)

## Future Improvements (If Needed)

### Potential Enhancements
1. **Full automation** - Add Selenium/Playwright to scraper for athlete data
2. **Timezone conversion** - Show times in user's local timezone
3. **Push notifications** - Alert when Estonia wins a medal
4. **Historical data** - Archive results after Olympics end
5. **Snowflake performance** - Reduce frequency on mobile detection
6. **Live countdown** - Timer to next Estonian event
7. **Social sharing** - Share Estonia's medal count on social media
8. **Multi-language** - Add English/Russian translations

### Code Organization
- Currently: Single-file architecture (simple, no build process)
- If expanding: Consider modular JavaScript (ES6 modules)
- If adding backend: Consider API for real-time updates

## Troubleshooting

### Snowflakes Not Showing
1. Check medal count in `data.json` (must be > 0 OR Feb 22, 2026)
2. Check browser console for JavaScript errors
3. Verify `data.json` is valid JSON (use JSONLint.com)
4. Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

### Site Not Updating After Push
1. Check GitHub Actions: https://github.com/emoggio/EstonianMedalist-/actions
2. Wait 2-3 minutes for GitHub Pages rebuild
3. Hard refresh browser (clear cache)
4. Check commit went to `main` branch

### Scraper Not Running
1. Check Actions permissions in repo settings
2. Check workflow file: `.github/workflows/update-results.yml`
3. Manually trigger from Actions tab
4. Check logs for Python errors

### Local Server Issues
1. Port 8000 already in use: Try `python -m http.server 8001`
2. Python not found: Install Python 3.x
3. CORS errors: Must use local server, not `file://`

## Contact & Maintenance

- **Owner**: emoggio (GitHub)
- **Created**: February 9, 2026
- **Olympics Dates**: February 6-22, 2026
- **Maintenance**: Update athlete data as events complete

## Quick Reference Commands

```bash
# Local testing
cd C:\Users\eu.moggio\Desktop\Olympics
python -m http.server 8000
# Open: http://localhost:8000

# Push changes
git add .
git commit -m "Your message"
git push origin main

# Test scraper locally
python scraper.py

# Check git status
git status

# View recent commits
git log --oneline -5

# Hard refresh browser
# Windows: Ctrl + F5
# Mac: Cmd + Shift + R
```

## Important Files to Never Commit

Already in `.gitignore`:
- `.claude/` - Claude Code local files
- `*.local.md` - Local configuration
- `.claude_history` - Chat history
- `__pycache__/` - Python cache
- `*.pyc` - Python compiled files

## End of Olympics (After Feb 22, 2026)

### Archive Steps
1. Take final screenshot of site
2. Export `data.json` as backup
3. Consider stopping GitHub Actions workflow (optional)
4. Add "Olympics Concluded" banner to site (optional)
5. Keep site live as historical record

### To Disable Auto-Updates
Edit `.github/workflows/update-results.yml`:
- Comment out the `schedule:` section
- Keep `workflow_dispatch:` for manual triggers

---

**Last Updated**: February 9, 2026
**Status**: Active - Olympics in progress
**Next Review**: After February 22, 2026

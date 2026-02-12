# Estonia at Cortina 2026 Olympics

A minimal, mobile-friendly website to track Estonia's performance at the Cortina 2026 Winter Olympics.

## Features

- **Medal Status**: Shows "Yes" or "No" if Estonia has won any medals
- **Medal Counter**: Displays gold, silver, and bronze medal counts
- **Completed Events**: Lists Estonian athletes who have finished competing (with medal indicators)
- **Upcoming Events**: Shows athletes yet to compete
- **Cortina 2026 Design**: Uses the official color scheme (blues, whites, ice tones)
- **Mobile Responsive**: Works perfectly on all devices
- **Manual Updates**: Update `data.json` on GitHub to add results (automated scraping currently blocked)

## Automated Updates

✅ **Now Using Wikipedia as Primary Data Source**

The scraper uses Wikipedia's Estonia at the 2026 Winter Olympics page as the main data source, providing reliable and comprehensive updates!

### What Gets Auto-Updated

✅ **Medal Detection** - Automatically monitors Wikipedia for Estonian medal wins
- Scraper runs every 1 hour checking Wikipedia's infobox and medal tables
- Updates medal counts automatically when Estonia wins
- Most reliable source for official medal tallies

⚠️ **Semi-Automated Athlete Results** - Scraper detects results from Wikipedia tables
- Parses competitor tables and results sections
- Extracts placements and medal information
- Requires manual review for accuracy

### What Needs Manual Updates

📝 **Athlete Details** - Requires manual updates to `data.json`:
- Moving athletes from "upcoming" to "completed"
- Adding specific competition results and placements
- Updating event schedules if changed

**Data Source**: [Wikipedia - Estonia at the 2026 Winter Olympics](https://en.wikipedia.org/wiki/Estonia_at_the_2026_Winter_Olympics) - Comprehensive, community-maintained coverage with official results.

### How It Works

1. **GitHub Actions Workflow** (`.github/workflows/update-results.yml`) runs every 1 hour
2. **Wikipedia Scraper** (`scraper_wikipedia.py`) fetches Wikipedia's Estonia Olympics page
3. **Infobox Parser**: Extracts official medal counts from Wikipedia's infobox
4. **Table Parser**: Parses competitor tables and results sections for athlete data
5. **Smart Detection**: Identifies athletes, sports, results, and medal winners
6. **Medal Updates**: Automatically updates medal counts when Estonia wins
7. **Auto-commit**: If medals change, the bot commits to your repository
8. **GitHub Pages**: Your site automatically updates with the latest data

**Data Source**: Wikipedia - Community-maintained, comprehensive coverage with official Olympic results.

**Update Frequency**: Every hour (24 checks per day for reliable updates)

### Manual Trigger

You can manually trigger an update:
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Update Estonia Olympic Results" workflow
4. Click "Run workflow"

## How to Update Data Manually

When Estonian athletes compete or win medals, update `data.json` on GitHub:

### Quick Update Link

🔗 **Direct edit link**: `https://github.com/emoggio/EstonianMedalist-/edit/main/data.json`

### Updating Medal Counts

1. Go to [data.json](https://github.com/emoggio/EstonianMedalist-/edit/main/data.json)
2. Update the `medals` section:
   ```json
   "medals": {
     "gold": 0,
     "silver": 0,
     "bronze": 0
   }
   ```
3. Commit changes
4. Site updates in 1-2 minutes

### Moving Athletes from Upcoming to Completed

1. Go to your repository: `https://github.com/YOUR_USERNAME/EstonianMedalist-`
2. Click on `data.json`
3. Click the pencil icon (Edit)
4. Move the athlete object from `"upcoming"` to `"completed"`
5. Add a `"result"` field with their placement
6. Add a `"medal"` field if they won (gold/silver/bronze)
7. Commit changes

### Example: Adding Completed Events
```json
{
  ...
  "completed": [
    {
      "name": "Kristjan Ilves",
      "sport": "Alpine Skiing",
      "medal": "gold"
    },
    {
      "name": "Johanna Talihärm",
      "sport": "Cross-Country Skiing"
    }
  ],
  ...
}
```

Valid medal values: `"gold"`, `"silver"`, `"bronze"`, or omit for no medal.

### Example: Adding Upcoming Events
```json
{
  ...
  "upcoming": [
    {
      "name": "Kelly Sildaru",
      "sport": "Freestyle Skiing"
    }
  ]
}
```

## Hosting on GitHub Pages

### 1. Create a new repository on GitHub

Create a new **public** repository (required for GitHub Actions on free tier).

### 2. Push these files to the repository

```bash
git init
git add .
git commit -m "Initial commit: Estonia Olympics tracker"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

### 3. Enable GitHub Actions Permissions

**IMPORTANT**: To allow the automated scraper to commit updates:

1. Go to your repository on GitHub
2. Go to **Settings** → **Actions** → **General**
3. Scroll to "Workflow permissions"
4. Select **"Read and write permissions"**
5. Check **"Allow GitHub Actions to create and approve pull requests"**
6. Click **Save**

### 4. Enable GitHub Pages

1. Go to your repository **Settings**
2. Navigate to **"Pages"** section
3. Under "Source", select **"main"** branch
4. Click **Save**

### 5. Your site is live!

Your site will be available at: `https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/`

The GitHub Action will start running automatically every 3 hours to update results.

## Local Testing

Simply open `index.html` in your web browser to test locally.

## Auto-refresh

The page automatically refreshes data every 5 minutes when open.

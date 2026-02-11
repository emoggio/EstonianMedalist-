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

## Automated Updates (Currently Limited)

⚠️ **Important**: Olympics.com is currently blocking automated scraping (403 Forbidden). Until this is resolved, all updates must be done manually.

### What Gets Auto-Updated

❌ **Medal Counts** - Currently blocked by Olympics.com anti-scraping measures
- Scraper runs every 3 hours but cannot access data
- Will automatically resume when access is restored

### What Needs Manual Updates

📝 **All Data** - Currently requires manual updates to `data.json`:
- Medal counts (gold, silver, bronze)
- Moving athletes from "upcoming" to "completed"
- Adding competition results
- Updating event schedules

**Why?** Olympics.com is actively blocking automated access with 403 Forbidden errors. This is common for high-traffic events. We're monitoring the situation and the scraper will automatically resume when access is restored.

### How It Works (When Scraping is Available)

1. **GitHub Actions Workflow** (`.github/workflows/update-results.yml`) runs every 3 hours
2. **Python Scraper** (`scraper.py`) attempts to fetch medal counts from Olympics.com
3. **Smart Merging**: Updates medals when available, preserves your manually curated athlete data
4. **Auto-commit**: If data changes, the bot commits to your repository
5. **GitHub Pages**: Your site automatically updates with the latest data

**Current Status**: Scraper runs but Olympics.com blocks access. Data must be manually updated.

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

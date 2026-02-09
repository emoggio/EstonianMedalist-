# Estonia at Cortina 2026 Olympics

A minimal, mobile-friendly website to track Estonia's performance at the Cortina 2026 Winter Olympics.

## Features

- **Medal Status**: Shows "Yes" or "No" if Estonia has won any medals
- **Medal Counter**: Displays gold, silver, and bronze medal counts
- **Completed Events**: Lists Estonian athletes who have finished competing (with medal indicators)
- **Upcoming Events**: Shows athletes yet to compete
- **Cortina 2026 Design**: Uses the official color scheme (blues, whites, ice tones)
- **Mobile Responsive**: Works perfectly on all devices
- **Automated Updates**: GitHub Actions automatically scrapes Olympics.com every 3 hours

## Automated Updates

This website uses GitHub Actions to automatically fetch and update Estonia's Olympic results every 3 hours. The scraper runs in the cloud and commits changes when new results are available.

### How It Works

1. **GitHub Actions Workflow** (`.github/workflows/update-results.yml`) runs every 3 hours
2. **Python Scraper** (`scraper.py`) fetches data from Olympics.com
3. **Auto-commit**: If medal counts or results change, the bot commits to your repository
4. **GitHub Pages**: Your site automatically updates with the latest data

### Manual Trigger

You can manually trigger an update:
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Update Estonia Olympic Results" workflow
4. Click "Run workflow"

## How to Update Data Manually

Edit the `data.json` file to update the information:

### Example: Adding Medals
```json
{
  "medals": {
    "gold": 1,
    "silver": 2,
    "bronze": 1
  },
  ...
}
```

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

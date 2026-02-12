# Quick Setup Guide

Follow these steps to deploy your automated Estonia Olympics tracker:

## Step 1: Test Locally (Optional)

Before deploying, you can test the scraper locally:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the scraper
python scraper.py

# Open index.html in your browser to see the results
```

## Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new **public** repository
2. Name it something like `estonia-olympics-2026`
3. Don't initialize with README (we already have files)

## Step 3: Push to GitHub

Run these commands in your Olympics folder:

```bash
git init
git add .
git commit -m "Initial commit: Estonia Olympics tracker with auto-updates"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values.

## Step 4: Configure GitHub Actions

⚠️ **CRITICAL STEP** - Without this, auto-updates won't work!

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Actions** → **General** (left sidebar)
4. Scroll to **"Workflow permissions"**
5. Select **"Read and write permissions"**
6. Check ✅ **"Allow GitHub Actions to create and approve pull requests"**
7. Click **Save**

## Step 5: Enable GitHub Pages

1. Still in **Settings**, click **Pages** (left sidebar)
2. Under **"Source"**, select branch: **main**
3. Keep folder as **/ (root)**
4. Click **Save**

## Step 6: Wait for Deployment

GitHub will build your site (takes 1-2 minutes). Your site will be live at:

```
https://YOUR_USERNAME.github.io/YOUR_REPO_NAME/
```

## Step 7: Verify Auto-Updates Work

1. Go to **Actions** tab in your repository
2. You should see the workflow "Update Estonia Olympic Results"
3. Click **"Run workflow"** → **"Run workflow"** to test it manually
4. Wait for it to complete (green checkmark)
5. Check if `data.json` was updated with a new commit

## Troubleshooting

### Workflow Not Running
- Make sure you enabled "Read and write permissions" in Step 4
- Make sure your repository is **public** (GitHub Actions has limited minutes on private repos)

### Site Not Updating
- GitHub Actions commits changes, but Pages might take 1-2 minutes to rebuild
- Check the Actions tab for any failed runs

### Manual Updates
If you want to update data manually instead of waiting for the scraper:
1. Edit `data.json` directly on GitHub or locally
2. Commit and push the changes
3. GitHub Pages will update automatically

## Schedule

The scraper runs:
- ⏰ Every 1 hour automatically
- 🔄 Can be triggered manually from Actions tab
- 📊 Only commits if data actually changed
- 📖 Uses Wikipedia as primary data source

Enjoy tracking Estonia's Olympic journey! 🇪🇪 🏔️

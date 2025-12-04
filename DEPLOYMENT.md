# Deployment Guide

## Quick Deployment on Vercel (Recommended)

### Step 1: Deploy via Vercel Dashboard (Easiest)
1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New Project"**
3. Select **"Import Git Repository"**
4. Paste: `https://github.com/Amar03ete/Metadata-Extractor.git`
5. Click **"Import"**
6. Vercel will auto-detect the `vercel.json` configuration
7. Click **"Deploy"**

**That's it!** Your app will be live at `https://metadata-extractor-xxx.vercel.app`

### Step 2: Configure Environment (Optional)
No environment variables needed! The app works out of the box.

---

## Deploy via Vercel CLI (Advanced)

```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy
cd "d:\python projects\meta data"
vercel --prod
```

---

## How It Works on Vercel

✓ **Frontend**: Static files served from `/frontend/index.html`
✓ **Backend**: Serverless Python functions in `/api/index.py` (max 60 seconds execution)
✓ **Storage**: Temporary files auto-cleaned after each request
✓ **CORS**: Enabled for all origins

**No servers to manage. Auto-scaling. Always on.**

---

## Local Testing (Before Deploying)

```bash
# Install Vercel CLI for local testing
npm i -g vercel

# Run locally on port 3000
vercel dev

# Frontend: http://localhost:3000
# API: http://localhost:3000/api/health
```

---

## Live Application

After deployment, your app is always active at the Vercel URL.

To use:
1. Visit your Vercel deployment URL
2. Upload a file
3. Get instant forensic analysis
4. Download JSON report

---

## Troubleshooting Vercel Deployment

**"Build Failed" Error?**
- Check that `vercel.json` exists
- Ensure `backend/requirements.txt` is valid
- Verify all Python files have no syntax errors

**"Function Timeout" (504 Error)?**
- Files larger than ~10MB might timeout
- Increase timeout in `vercel.json` (max 60s)

**"Cold Start" (First Request Slow)?**
- Vercel cold starts can take 5-10 seconds
- Subsequent requests are faster (~1-2s)
- Use Vercel Pro for faster cold starts

**Missing Modules?**
- Ensure all imports are in `backend/requirements.txt`
- Run `pip install -r backend/requirements.txt` locally to verify

---

## Redeploy After Code Changes

Simply push to GitHub:
```bash
git add .
git commit -m "Update deployment"
git push origin master
```

Vercel will automatically detect changes and redeploy!

---

## Keep App Always Active

With Vercel, your app is always on!

- **Frontend**: Served 24/7 from Vercel's CDN
- **API**: Cold starts (1-5s on first request, then fast)
- **Cron Jobs** (Optional): Ping your API every 5 minutes to avoid cold starts

To keep warm, add to GitHub Actions (`.github/workflows/keep-alive.yml`):
```yaml
name: Keep Vercel App Warm
on:
  schedule:
    - cron: '*/5 * * * *'
jobs:
  warm:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Vercel App
        run: curl https://your-app.vercel.app/api/health
```

---

## Next Steps

1. ✅ Code is ready (vercel.json, api/index.py, frontend updated)
2. ✅ Git repo has all files
3. Next: Push to GitHub → Vercel auto-deploys
4. Share your live URL!

**Your app will be production-ready and always accessible!**

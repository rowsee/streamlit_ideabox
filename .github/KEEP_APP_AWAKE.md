# Keep App Awake - Setup Guide

Your Streamlit app on the free tier will sleep after periods of inactivity. This guide shows you how to keep it awake using multiple methods.

## Current Setup: GitHub Actions (Primary)

A GitHub Actions workflow is configured to ping your app every 3 minutes.

### Workflow Details
- **File:** `.github/workflows/ping.yml`
- **Frequency:** Every 3 minutes (180 pings/day)
- **Method:** HTTP GET requests with browser-like headers
- **Cost:** Free (uses GitHub Actions free tier)

### How It Works
1. Runs automatically every 3 minutes
2. Sends 2 ping attempts per run (30 seconds apart)
3. Uses realistic browser headers to avoid detection
4. Adds random query parameters to prevent caching

### Monitoring
Check the workflow status:
1. Go to GitHub → Your Repo → Actions
2. Look for "Keep App Awake" workflow
3. Check recent runs show green checkmarks ✅

---

## Backup Setup: Better Uptime (Recommended)

If GitHub Actions alone isn't keeping the app awake, add Better Uptime as a backup.

### Setup Instructions

1. **Sign up at https://betteruptime.com**
   - Click "Sign up free"
   - Use your email or GitHub account

2. **Create a new monitor**
   - Click "New Monitor"
   - Monitor Type: **URL**
   - URL: `https://procurementideabox.streamlit.app`
   - Monitoring Interval: **3 minutes** (most frequent on free tier)

3. **Configure settings**
   - Request Timeout: 30 seconds
   - Expected Status Code: 200
   - Follow Redirects: Yes

4. **Optional: Set up notifications**
   - Add your email for downtime alerts
   - This is useful to know if the app goes down

5. **Save the monitor**

### Cost
- **Free tier:** Unlimited monitors, 3-minute intervals
- No credit card required

---

## Alternative Services (Choose One)

### Option A: UptimeRobot (Most Popular)
- **Website:** https://uptimerobot.com
- **Free tier:** 50 monitors, 5-minute intervals
- Good for simple monitoring

### Option B: Cron-Job.org (Most Frequent)
- **Website:** https://cron-job.org
- **Free tier:** Unlimited jobs, 1-minute intervals
- Most frequent pings available

### Option C: Pingdom (Enterprise Grade)
- **Website:** https://www.pingdom.com
- **Free tier:** 1 monitor, 60-minute intervals
- Less frequent but very reliable

---

## Why Apps Still Sleep (Troubleshooting)

Even with pinging, apps may sleep because:

### 1. Streamlit Detects Automated Traffic
**Solution:** The updated workflow now uses realistic browser headers

### 2. Insufficient Traffic Volume
**Solution:** Use multiple services (GitHub Actions + Better Uptime)

### 3. App Errors or Crashes
**Solution:** Check Streamlit logs in the dashboard

### 4. GitHub Actions Paused
**Solution:** GitHub pauses workflows after 60 days of repo inactivity
- Push any commit to reactivate
- Or manually trigger from Actions tab

---

## Verification

Test if your app stays awake:

1. **Wait Test**
   - Open: https://procurementideabox.streamlit.app
   - Wait 10-15 minutes without interaction
   - Refresh the page
   - ✅ Pass: Loads immediately
   - ❌ Fail: Shows "Please wait..." spinner

2. **Next Morning Test**
   - Check app first thing in the morning
   - Should load without delay

---

## Monthly Usage

### GitHub Actions
- **Minutes used:** ~43,200 seconds (12 hours) per month
- **Free tier limit:** 2,000 minutes (33 hours) per month
- **Status:** ✅ Well within limits

### Better Uptime
- **Requests:** ~14,400 per month (3-min intervals)
- **Free tier limit:** Unlimited
- **Status:** ✅ Unlimited on free tier

---

## Recommended Configuration

**Primary:** GitHub Actions (every 3 minutes)
**Backup:** Better Uptime (every 3 minutes)

This dual-setup ensures if one service fails or is blocked, the other keeps the app awake.

---

## Emergency: App Won't Wake Up

If the app consistently goes to sleep:

1. **Check workflow status**
   ```
   GitHub → Actions → Keep App Awake
   ```

2. **Test manually**
   ```bash
   curl -I https://procurementideabox.streamlit.app
   ```

3. **Check Streamlit dashboard**
   ```
   https://share.streamlit.io/
   ```
   Look for error messages or warnings

4. **Enable both services**
   - Keep GitHub Actions
   - Add Better Uptime
   - Wait 15 minutes and test

5. **Contact Streamlit Support**
   - If nothing works, reach out to support@streamlit.io
   - They may have implemented new sleep policies

---

## Updates

Last updated: 2025-01-XX

If Streamlit changes their sleep policies, this document will be updated with new solutions.

# 🚀 IoT Sentinel - Complete Deployment Guide

This guide walks you through deploying IoT Sentinel to Render's free tier.

---

## 📋 Prerequisites

- GitHub account
- Render account (free at [render.com](https://render.com))
- Git installed locally (optional, for pushing changes)

---

## 🎯 Step 1: Prepare Your Repository

### Option A: Push Existing Code to GitHub

```bash
# Navigate to the project directory
cd "D:\Aditya\Hackathon Code\Team Rocket\iot_sentinel"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial IoT Sentinel deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/iot-sentinel.git

# Push to GitHub
git push -u origin main
```

### Option B: Create New GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `iot-sentinel`
3. Description: "IoT Anomaly Detection with Shodan-style Dashboard"
4. Public repository
5. Click **Create repository**
6. Follow the push commands shown

---

## 🌐 Step 2: Deploy to Render

### 2.1 Sign Up for Render

1. Visit [render.com](https://render.com)
2. Click **Get Started for Free**
3. Sign up with GitHub (recommended) or email

### 2.2 Create New Web Service

1. Click **New +** → **Web Service**
2. Connect your GitHub account
3. Find and select your `iot-sentinel` repository
4. Click **Connect**

### 2.3 Configure the Service

Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `iot-sentinel` (or your choice) |
| **Region** | Oregon (closest to you) |
| **Branch** | `main` |
| **Root Directory** | (leave blank) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `bash start.sh` |

### 2.4 Configure Free Tier

| Setting | Value |
|---------|-------|
| **Instance Type** | **Free** |
| **Auto-Deploy** | ✅ Enabled |

### 2.5 Add Environment Variables

Click **Advanced** → **Add Environment Variable**:

```
KEY: PORT
VALUE: 10000

KEY: HOST
VALUE: 0.0.0.0

KEY: RELOAD
VALUE: false

KEY: RENDER
VALUE: true
```

### 2.6 Add Disk (Optional but Recommended)

Click **Add Disk**:

| Setting | Value |
|---------|-------|
| **Name** | `iot-data` |
| **Mount Path** | `/opt/render/project/src/data` |
| **Size** | `1 GB` (free tier limit) |

### 2.7 Deploy!

1. Click **Create Web Service**
2. Wait for build (2-5 minutes)
3. Once deployed, you'll see your app URL

---

## 🎨 Step 3: Access Your Dashboard

Your dashboard will be available at:

```
https://iot-sentinel-XXXX.onrender.com
```

Replace `XXXX` with your unique Render subdomain.

### Test the Dashboard

1. **Open the URL** in your browser
2. **Click "Generate Test Alert"** to see real-time detection
3. **Click "Run ML Model (IoT-2023)"** to batch process demo data
4. **Upload a dataset** using the upload button

---

## 📡 Step 4: Test API Endpoints

### Health Check

```bash
curl https://iot-sentinel-XXXX.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "timestamp": "2024-..."
}
```

### API Documentation

Visit: `https://iot-sentinel-XXXX.onrender.com/api/docs`

### Batch Score Test

```bash
curl -X POST https://iot-sentinel-XXXX.onrender.com/api/batch-score
```

### Network Topology

```bash
curl https://iot-sentinel-XXXX.onrender.com/api/network-topology
```

---

## 🔧 Step 5: Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError: No module named 'aiofiles'`

**Solution**: Ensure `requirements.txt` includes all dependencies:
```
fastapi
uvicorn[standard]
aiofiles
python-multipart
...
```

### Service Won't Start

**Error**: `start.sh: Permission denied`

**Solution**: Render should handle this, but verify your `start.sh` is in the repo.

### Model Not Loading

**Check logs** in Render dashboard:
1. Go to your service
2. Click **Logs** tab
3. Look for "Engine loaded" messages

**Solution**: Model files should be in `models/` directory:
- `isolation_forest.pkl`
- `scaler.pkl`
- `metadata.json`

### WebSocket Won't Connect

**Free Tier Limitation**: Render's free tier may have WebSocket limitations.

**Workaround**: The dashboard will still work with polling fallback.

### Service Goes to Sleep

**Free Tier Limitation**: Free services sleep after 15 minutes of inactivity.

**Solution**: 
1. Visit the dashboard every 15 minutes
2. Use a free uptime monitor (e.g., UptimeRobot)
3. Upgrade to paid tier for always-on

---

## 📊 Step 6: Upload Your Dataset

### Via Dashboard (Recommended)

1. Open your dashboard
2. Scroll to **Upload Dataset** section
3. Drag & drop your CSV or Zeek log file
4. Click **Run ML Model (IoT-2023)** to process

### Via API

```bash
curl -X POST \
  -F "file=@your-dataset.csv" \
  https://iot-sentinel-XXXX.onrender.com/api/upload
```

Then trigger batch processing:
```bash
curl -X POST https://iot-sentinel-XXXX.onrender.com/api/batch-score
```

---

## 🔄 Step 7: Update Your Deployment

### Automatic Deployment (Recommended)

With **Auto-Deploy** enabled:

1. Make changes locally
2. `git add . && git commit -m "Update"`
3. `git push`
4. Render automatically rebuilds and deploys (2-3 minutes)

### Manual Redeploy

1. Go to Render dashboard
2. Select your service
3. Click **Manual Deploy** → **Deploy latest commit**

---

## 📈 Step 8: Monitor Your Application

### Render Dashboard

- **Metrics**: CPU, Memory, Request count
- **Logs**: Real-time application logs
- **Deploys**: Deployment history

### Application Metrics

Visit: `https://iot-sentinel-XXXX.onrender.com/metrics`

### Health Monitoring

Set up alerts using:
- **UptimeRobot** (free): Monitor `/health` endpoint
- **Render Notifications**: Enable in dashboard settings

---

## 🎓 Tips for Hackathon Demo

### 1. Pre-load Demo Data

Before presenting:
```bash
# Trigger batch processing to populate dashboard
curl -X POST https://iot-sentinel-XXXX.onrender.com/api/batch-score
```

### 2. Keep Service Awake

Use a free uptime monitor to ping every 10 minutes:
- UptimeRobot: https://uptimerobot.com
- Set HTTP check on `/health`

### 3. Prepare Demo Script

1. **Open dashboard** - Show the Shodan-style UI
2. **Generate test alert** - Click button for instant result
3. **Run ML model** - Process IoT-2023 dataset
4. **Show network map** - Explain topology visualization
5. **Upload dataset** - Demo file upload feature
6. **API docs** - Show `/api/docs` for completeness

### 4. Backup Plan

If Render is slow:
- Have screenshots ready
- Run locally as backup: `bash start_all.bat`

---

## 🆘 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Build timeout | Check file sizes, remove large files from git |
| 502 Bad Gateway | Wait 2-3 minutes for cold start |
| WebSocket fails | Dashboard has fallback, still functional |
| Model missing | Push model files to GitHub or train offline |
| Upload fails | Check file size < 50MB, verify format |

---

## 📞 Getting Help

### Render Support
- **Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

### Project Issues
- Check `dashboard.log` for errors
- Review API logs in Render dashboard
- Test locally first: `bash start_all.bat`

---

## ✅ Deployment Checklist

- [ ] GitHub repository created
- [ ] Render account set up
- [ ] Web service created on Render
- [ ] Environment variables configured
- [ ] Disk mounted (optional)
- [ ] Build successful
- [ ] Health check passes
- [ ] Dashboard loads
- [ ] WebSocket connects (or fallback works)
- [ ] API documentation accessible
- [ ] Test data generated successfully
- [ ] Upload feature tested
- [ ] Monitoring set up

---

## 🎉 You're Deployed!

Your IoT Sentinel is now live on Render's free tier!

**Share your dashboard**: `https://iot-sentinel-XXXX.onrender.com`

**Good luck with your hackathon!** 🚀

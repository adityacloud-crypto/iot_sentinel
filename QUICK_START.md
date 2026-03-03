# 🎯 IoT Sentinel - Quick Start Guide

**5-Minute Setup for Hackathon Demo**

---

## 🚀 Option 1: Deploy to Render (Recommended)

### Step 1: Push to GitHub (2 minutes)

```bash
cd "D:\Aditya\Hackathon Code\Team Rocket\iot_sentinel"

# Initialize git if needed
git init
git add .
git commit -m "IoT Sentinel ready for hackathon"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/iot-sentinel.git
git push -u origin main
```

### Step 2: Deploy to Render (3 minutes)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click **New +** → **Web Service**
4. Connect your `iot-sentinel` repository
5. Use these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Instance**: Free tier
6. Click **Create Web Service**

### Step 3: Wait & Access (2-5 minutes)

Your dashboard will be live at:
```
https://iot-sentinel-XXXX.onrender.com
```

---

## 💻 Option 2: Run Locally

### Windows (1 minute)

```bash
cd "D:\Aditya\Hackathon Code\Team Rocket\iot_sentinel"

# Activate virtual environment
venv\Scripts\activate

# Run the application
start_all.bat
```

### Linux/macOS

```bash
cd iot_sentinel
source venv/bin/activate
bash start.sh
```

**Access**: http://localhost:8000

---

## 🎨 Dashboard Features

### Try These Buttons:

1. **🔺 Generate Test Alert** - Creates anomalous traffic, shows instant detection
2. **✓ Generate Normal Traffic** - Creates normal traffic patterns
3. **▶ Run ML Model (IoT-2023)** - Batch processes 50 sample records
4. **📤 Upload Dataset** - Drag & drop your CSV/Zeek files

### Watch For:

- **Network Topology Map** - Animated device graph
- **Trust Score Timeline** - Real-time chart updates
- **Verdict Badges** - Color-coded threat classification
- **Device Table** - Per-device health monitoring

---

## 📡 API Testing

### Quick Tests

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/api/docs

# Batch score test
curl -X POST http://localhost:8000/api/batch-score

# Network topology
curl http://localhost:8000/api/network-topology
```

---

## 🎯 Hackathon Demo Flow (2 minutes)

### 1. Open Dashboard (10 seconds)
```
https://your-app.onrender.com
```

### 2. Generate Live Alert (20 seconds)
- Click **"Generate Test Alert"**
- Watch real-time WebSocket update
- Point out trust score drop and ANOMALY verdict

### 3. Run Batch Analysis (30 seconds)
- Click **"Run ML Model (IoT-2023)"**
- Show progress in timeline chart
- Highlight device table filling up

### 4. Show Network Map (30 seconds)
- Scroll to **Network Topology Map**
- Explain animated nodes (green=normal, red=anomaly)
- Show legend and device connections

### 5. Upload Dataset (30 seconds)
- Scroll to **Upload Dataset**
- Drag & drop a CSV file
- Show upload progress bar

### 6. API Documentation (20 seconds)
- Navigate to `/api/docs`
- Show complete REST API
- Mention enterprise integration ready

---

## 🏆 Key Selling Points

### For Judges:

✅ **Real ML** - Isolation Forest anomaly detection
✅ **Beautiful UI** - Shodan-style professional dashboard
✅ **Real-time** - WebSocket streaming updates
✅ **Production Ready** - Deployed on cloud (Render)
✅ **Zero Cost** - Runs on free tier
✅ **Complete API** - REST + WebSocket + Docs

### Technical Highlights:

- **Unsupervised Learning** - Detects zero-day attacks
- **Multi-factor Scoring** - ML + Rules + Entropy
- **Explainable AI** - Risk factors and confidence %
- **Network Visualization** - Interactive topology map
- **Dataset Agnostic** - Supports multiple formats

---

## 🐛 Troubleshooting

### Render Deployment Issues

**Build Failed**: Check logs in Render dashboard
**Service Sleeping**: Free tier sleeps after 15 min - visit to wake
**WebSocket Fails**: Dashboard has fallback, still functional

### Local Issues

**Module Not Found**: Activate venv, run `pip install -r requirements.txt`
**Port in Use**: Change PORT in start.sh or use different port
**Model Missing**: Run `python src/train.py` to generate models

---

## 📊 Dataset Information

### Using CTU-IoT-23 Dataset

**Download**: https://www.stratosphereips.org/datasets-iot23

**Files Needed**:
- `CTU-Honeypot-Capture-4-1/bro/conn.log.labeled`
- `CTU-IoT-Malware-Capture-1-1/bro/conn.log.labeled`

**Process**:
```bash
python src/data_pipeline.py
python src/train.py
```

---

## 🎤 Elevator Pitch (30 seconds)

> "IoT Sentinel is a real-time network intrusion detection system for IoT devices. Using unsupervised machine learning, it detects anomalies without needing labeled training data - meaning it can identify zero-day attacks. The Shodan-style dashboard provides beautiful real-time visualization of network health, while the REST API enables enterprise integration. Best of all, it runs on free infrastructure, making enterprise-grade IoT security accessible to everyone."

---

## 📞 Support

**Documentation**: See README.md
**Deployment Guide**: See DEPLOYMENT_GUIDE.md
**Presentation**: See HACKATHON_PRESENTATION.md

---

## ✅ Pre-Demo Checklist

- [ ] Dashboard loads successfully
- [ ] "Generate Test Alert" button works
- [ ] "Run ML Model" processes data
- [ ] Network topology map displays
- [ ] WebSocket shows "Connected" (green)
- [ ] API docs accessible at /api/docs
- [ ] Upload feature tested
- [ ] Backup screenshots ready

---

**Good luck with your hackathon! 🛡️🚀**

*You're all set to impress the judges!*

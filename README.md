# 🛡️ IoT Sentinel - Enterprise IoT Anomaly Detection System

A production-grade, real-time network intrusion detection system for IoT device fleets using unsupervised machine learning (Isolation Forest), heuristic rule engines, and entropy-based traffic analysis.

![IoT Sentinel](https://img.shields.io/badge/IoT-Security-e74c3c?style=for-the-badge)
![ML Model](https://img.shields.io/badge/ML-Isolation%20Forest-3498db?style=for-the-badge)
![Deployment](https://img.shields.io/badge/Deploy-Render-27ae60?style=for-the-badge)

## 🌟 Features

- **Real-time Anomaly Detection** - Detect IoT device threats in real-time using ML
- **Shodan-style Dashboard** - Beautiful network security visualization
- **Network Topology Map** - Interactive device relationship graph
- **Dataset Upload** - Upload custom IoT datasets (CSV, Zeek format)
- **Batch Processing** - Run ML model on entire datasets
- **WebSocket Streaming** - Live threat broadcasts to all connected clients
- **RESTful API** - Complete API with Swagger documentation
- **Free Tier Ready** - Optimized for Render's free tier (512MB RAM)

## 🚀 Quick Start - Deploy to Render

### Option 1: One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Option 2: Manual Deployment

1. **Fork this repository** to your GitHub account

2. **Create a Render account** at [render.com](https://render.com)

3. **Create a new Web Service**:
   - Connect your GitHub repository
   - Choose **Python** runtime
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `bash start.sh`

4. **Configure Environment Variables**:
   ```
   PORT=10000
   HOST=0.0.0.0
   RELOAD=false
   RENDER=true
   ```

5. **Deploy** - Render will automatically build and deploy your application

6. **Access Dashboard** - Visit your Render URL to see the dashboard

## 📊 Dashboard Features

### Network Security Dashboard
- **Real-time Metrics** - Trust scores, anomaly rates, device health
- **Network Topology Map** - Visual device graph with threat indicators
- **Threat Timeline** - Historical trust score visualization
- **Device Health Monitor** - Per-device status and metrics
- **Risk Factor Analysis** - Breakdown of detected threats

### Interactive Controls
- **Upload Dataset** - Drag & drop CSV/Zeek files (max 50MB)
- **Run ML Model** - Process IoT-2023 dataset with one click
- **Generate Test Data** - Simulate normal/anomalous traffic
- **Search Devices** - Filter by device ID, IP, or threat type

## 📡 API Endpoints

### Core Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/score` | Score network telemetry |
| `GET` | `/health` | Health check |
| `WS` | `/ws` | WebSocket for real-time updates |

### Dataset Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload` | Upload dataset file |
| `POST` | `/api/batch-score` | Run batch ML analysis |
| `POST` | `/api/train` | Trigger model training |

### Network Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/network-topology` | Get network graph data |
| `GET` | `/api/devices` | List all devices |
| `GET` | `/api/threats` | Get threat intelligence |
| `GET` | `/api/device/{id}` | Get device details |

### Documentation
- **Swagger UI**: `/api/docs`
- **ReDoc**: `/api/redoc`

## 🔧 Local Development

### Prerequisites
- Python 3.11+
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd iot_sentinel

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Option 1: Use startup script (recommended)
# Windows
start_all.bat
# Linux/macOS
bash start.sh

# Option 2: Run components manually
# Start API server
uvicorn src.api_server:app --host 0.0.0.0 --port 8000

# Dashboard is served automatically at http://localhost:8000/
```

### Process Dataset (Optional)

```bash
# Download CTU-IoT-23 dataset from https://www.stratosphereips.org/datasets-iot23
# Place in data/raw/ directory

# Process the dataset
python src/data_pipeline.py

# Train the model
python src/train.py
```

## 📁 Project Structure

```
iot_sentinel/
├── src/
│   ├── api_server.py        # FastAPI server with all endpoints
│   ├── engine.py            # ML inference engine
│   ├── train.py             # Model training script
│   ├── data_pipeline.py     # Data preprocessing
│   ├── dataset_processor.py # Upload handling
│   └── network_viz.py       # Network topology visualization
├── static/
│   └── index.html           # Shodan-style dashboard
├── models/
│   ├── isolation_forest.pkl # Trained ML model
│   ├── scaler.pkl           # Feature scaler
│   └── metadata.json        # Model metadata
├── data/
│   ├── raw/                 # Raw datasets (not tracked)
│   ├── processed/           # Processed datasets
│   └── uploads/             # User uploads
├── render.yaml              # Render deployment config
├── start.sh                 # Startup script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## 🎯 Detection Capabilities

| Threat Type | Detection Method | Trust Score Range |
|-------------|------------------|-------------------|
| Data Exfiltration | ML + High Bytes | 15-35 |
| DDoS Flooding | ML + High Packets | 10-30 |
| Port Scanning | ML + S0 State | 25-45 |
| ICMP Flood | ML + ICMP Protocol | 20-40 |
| C2 Beaconing | ML Pattern Detection | 30-48 |

## 🧮 Scoring Formula

```
risk_score = 0.70 × ml_score + 0.20 × rule_score + 0.10 × entropy_score
trust_score = 100 - risk_score

Verdict Thresholds:
  >70  = NORMAL
  50-70 = SUSPICIOUS
  30-50 = RISKY
  ≤30  = ANOMALY
```

## 📊 Dataset Support

### Supported Formats
- **CTU-IoT-23** (Zeek conn.log format)
- **Edge-IIoTset** (CSV format)
- **Generic CSV** (with standard column names)
- **Zeek/Bro conn.log** (native format)

### Required Columns
- `duration` - Connection duration
- `orig_bytes` - Bytes sent from origin
- `resp_bytes` - Bytes sent from responder
- `orig_pkts` - Packets sent from origin
- `resp_pkts` - Packets sent from responder
- `proto` - Protocol (TCP/UDP/ICMP)
- `conn_state` - Connection state

## ☁️ Render Free Tier Optimization

This application is optimized for Render's free tier:

- **Memory**: < 512MB RAM usage
- **CPU**: Single worker process
- **Storage**: 1GB disk for data
- **Hours**: 750 hours/month (continuous deployment)

### Tips for Free Tier
1. Model files are pre-trained and included in the repo
2. Use batch processing sparingly (generates demo data if no upload)
3. WebSocket connections are ephemeral (reset on deploy)
4. Uploads are stored temporarily (cleared on restart)

## 🔒 Security Considerations

- **No Authentication** - Add authentication for production use
- **File Upload Limits** - 50MB max file size
- **Rate Limiting** - Install `slowapi` for production rate limiting
- **CORS** - Currently allows all origins (configure for production)

## 📈 Monitoring

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Metrics (Prometheus Format)
```bash
curl https://your-app.onrender.com/metrics
```

### JSON Metrics
```bash
curl https://your-app.onrender.com/metrics/json
```

## 🐛 Troubleshooting

### Model Not Loading
```
Solution: Ensure models/isolation_forest.pkl and models/scaler.pkl exist
Run: python src/train.py to generate models
```

### Upload Fails
```
Solution: Check file size (< 50MB) and format (CSV or Zeek log)
Verify column names match supported formats
```

### WebSocket Disconnected
```
Solution: Check browser console for errors
Verify server is running and accessible
Free tier may sleep after inactivity - trigger a request to wake
```

### Render Deployment Fails
```
Solution: Check build logs in Render dashboard
Verify requirements.txt has all dependencies
Ensure start.sh has execute permissions (chmod +x start.sh)
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System architecture and data flow
- [Threat Model](docs/THREAT_MODEL.md) - Detected threat categories
- [Dataset Strategy](docs/DATASET_STRATEGY.md) - Dataset selection rationale
- [Explainability](docs/EXPLAINABILITY.md) - Scoring explainability spec

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## 📄 License

This project is open-source and available for educational and hackathon purposes.

## 🏆 Hackathon Ready

This project is built for IoT security hackathons:

- ✅ **Quick Deployment** - One-click Render deployment
- ✅ **Impressive Demo** - Shodan-style dashboard with live updates
- ✅ **ML-Powered** - Real anomaly detection with Isolation Forest
- ✅ **Dataset Ready** - Supports CTU-IoT-23 and other IoT datasets
- ✅ **API Complete** - Full REST API with documentation
- ✅ **Free Tier** - Runs on Render's free tier

## 📞 Support

For issues or questions:
- Check the [Documentation](docs/)
- Review API docs at `/api/docs`
- Check Render deployment logs

---

**Built with ❤️ for IoT Security** | [Deploy to Render](https://render.com) | [API Docs](/api/docs)

# Data Directory

This directory stores IoT datasets for processing and analysis.

## Directory Structure

```
data/
├── raw/           # Raw uploaded datasets (not tracked in git)
├── processed/     # Processed datasets ready for training
└── uploads/       # User uploads from dashboard
```

## Downloading CTU-IoT-23 Dataset

1. Visit: https://www.stratosphereips.org/datasets-iot23

2. Download these captures:
   - **CTU-Honeypot-Capture-4-1** (benign baseline)
   - **CTU-IoT-Malware-Capture-1-1** (malware traffic)

3. Extract to `data/raw/` directory:
   ```
   data/raw/
   ├── CTU-Honeypot-Capture-4-1/
   │   └── bro/
   │       └── conn.log.labeled
   └── CTU-IoT-Malware-Capture-1-1/
       └── bro/
           └── conn.log.labeled
   ```

4. Process the dataset:
   ```bash
   python src/data_pipeline.py
   ```

## Supported Upload Formats

### CSV Format
- Standard CSV with column headers
- Required columns: duration, orig_bytes, resp_bytes, orig_pkts, resp_pkts, proto, conn_state

### Zeek/Bro Format
- Native conn.log format from Zeek/Bro
- Automatically detected by #fields line

### Edge-IIoTset Format
- Kaggle IoT dataset format
- Automatically mapped to standard columns

## File Size Limits

- Dashboard Upload: 50MB max
- Recommended: < 10MB for best performance
- Large datasets: Process offline with data_pipeline.py

"""
IoT Sentinel - Dataset Processor
Handles uploaded datasets for batch processing and analysis.
"""
import os
import logging
import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import tempfile
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatasetProcessor:
    """Process uploaded IoT datasets for batch analysis."""
    
    def __init__(self, upload_dir: str = "data/uploads", processed_dir: str = "data/processed"):
        self.upload_dir = Path(upload_dir)
        self.processed_dir = Path(processed_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Column mappings for different dataset formats
        self.column_mappings = {
            # CTU-IoT-23 format
            'ctu_iot': {
                'duration': ['duration', 'dur'],
                'orig_bytes': ['orig_bytes', 'orig_ip_bytes'],
                'resp_bytes': ['resp_bytes', 'resp_ip_bytes'],
                'orig_pkts': ['orig_pkts', 'orig_packets'],
                'resp_pkts': ['resp_pkts', 'resp_packets'],
                'proto': ['proto', 'protocol'],
                'conn_state': ['conn_state', 'state'],
                'label': ['label', 'Label', 'binary_label']
            },
            # Edge-IIoTset format
            'edge_iiot': {
                'duration': ['Duration'],
                'orig_bytes': ['data_pkt_size'],
                'resp_bytes': ['total_data_pkt_size'],
                'orig_pkts': ['pkt_size_avg'],
                'resp_pkts': ['pkt_size_std'],
                'proto': ['proto'],
                'conn_state': ['state'],
                'label': ['label', 'attack']
            },
            # Generic format
            'generic': {
                'duration': ['duration', 'time', 'dur'],
                'orig_bytes': ['orig_bytes', 'bytes_sent', 'sent_bytes'],
                'resp_bytes': ['resp_bytes', 'bytes_received', 'recv_bytes'],
                'orig_pkts': ['orig_pkts', 'packets_sent'],
                'resp_pkts': ['resp_pkts', 'packets_received'],
                'proto': ['proto', 'protocol'],
                'conn_state': ['conn_state', 'state', 'status'],
                'label': ['label', 'Label', 'anomaly', 'class']
            }
        }
    
    def save_upload(self, file_content: bytes, filename: str) -> str:
        """Save uploaded file to upload directory."""
        filepath = self.upload_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        with open(filepath, 'wb') as f:
            f.write(file_content)
        logger.info(f"Saved upload to {filepath}")
        return str(filepath)
    
    def detect_format(self, filepath: str) -> str:
        """Detect dataset format based on columns."""
        try:
            # Try reading first few lines
            if filepath.endswith('.log'):
                # Zeek conn.log format
                with open(filepath, 'r') as f:
                    first_line = f.readline()
                    if '#fields' in first_line:
                        return 'ctu_iot'
            
            # Try CSV
            df = pd.read_csv(filepath, nrows=10)
            columns = set(df.columns.str.lower())
            
            # Check for CTU-IoT format
            if 'orig_bytes' in columns and 'conn_state' in columns:
                return 'ctu_iot'
            
            # Check for Edge-IIoTset
            if 'duration' in columns and 'data_pkt_size' in columns:
                return 'edge_iiot'
            
            return 'generic'
        except Exception as e:
            logger.warning(f"Format detection failed: {e}")
            return 'generic'
    
    def load_dataset(self, filepath: str) -> Optional[pd.DataFrame]:
        """Load dataset from file."""
        try:
            if filepath.endswith('.log'):
                # Zeek conn.log format
                return self._load_zeek_log(filepath)
            else:
                # CSV format
                return pd.read_csv(filepath)
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            return None
    
    def _load_zeek_log(self, filepath: str) -> pd.DataFrame:
        """Load Zeek conn.log file."""
        fields_line = None
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('#fields'):
                    fields_line = line.strip()
                    break
        
        if not fields_line:
            raise ValueError("No #fields line found in Zeek log")
        
        columns = fields_line.replace('#fields', '').strip().split()
        
        df = pd.read_csv(
            filepath,
            sep=r'\s+',
            comment='#',
            header=None,
            names=columns,
            dtype=str,
            on_bad_lines='warn'
        )
        
        return df
    
    def normalize_columns(self, df: pd.DataFrame, format_type: str) -> pd.DataFrame:
        """Normalize column names based on detected format."""
        mappings = self.column_mappings.get(format_type, self.column_mappings['generic'])
        
        normalized = df.copy()
        for target_col, possibilities in mappings.items():
            for poss in possibilities:
                # Case-insensitive column search
                matching_cols = [c for c in df.columns if c.lower() == poss.lower()]
                if matching_cols:
                    normalized = normalized.rename(columns={matching_cols[0]: target_col})
                    break
        
        return normalized
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess data for scoring."""
        # Replace special values
        df = df.replace(['-', '(empty)', 'null', 'None'], pd.NA)
        
        # Convert numeric columns
        numeric_cols = ['duration', 'orig_bytes', 'resp_bytes', 'orig_pkts', 'resp_pkts']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Fill NaN with 0 for numeric columns
        for col in numeric_cols:
            if col in df.columns:
                df[col] = df[col].fillna(0)
        
        # Fill categorical columns
        for col in ['proto', 'conn_state']:
            if col in df.columns:
                df[col] = df[col].fillna('unknown')
        
        # Drop rows with missing critical fields
        if 'duration' in df.columns:
            df = df.dropna(subset=['duration'])
        
        return df
    
    def extract_scoring_rows(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Extract rows in format suitable for scoring API."""
        scoring_rows = []
        
        required_fields = ['duration', 'orig_bytes', 'resp_bytes', 'orig_pkts', 'resp_pkts', 'proto', 'conn_state']
        
        for idx, row in df.iterrows():
            try:
                # Check if we have minimum required fields
                if not all(field in row.index for field in required_fields):
                    continue
                
                # Validate numeric fields
                try:
                    duration = float(row.get('duration', 0))
                    orig_bytes = float(row.get('orig_bytes', 0))
                    resp_bytes = float(row.get('resp_bytes', 0))
                    orig_pkts = int(float(row.get('orig_pkts', 0)))
                    resp_pkts = int(float(row.get('resp_pkts', 0)))
                except (ValueError, TypeError):
                    continue
                
                # Normalize protocol
                proto = str(row.get('proto', 'TCP')).upper()
                if proto not in ['TCP', 'UDP', 'ICMP']:
                    proto = 'TCP'
                
                # Normalize connection state
                conn_state = str(row.get('conn_state', 'SF')).upper()
                valid_states = ['SF', 'S0', 'REJ', 'RST', 'SH', 'SHR', 'OTH']
                if conn_state not in valid_states:
                    conn_state = 'SF'
                
                scoring_row = {
                    'duration': duration,
                    'orig_bytes': orig_bytes,
                    'resp_bytes': resp_bytes,
                    'orig_pkts': max(0, orig_pkts),
                    'resp_pkts': max(0, resp_pkts),
                    'proto': proto,
                    'conn_state': conn_state,
                    'device_id': f'device_{idx % 20 + 1}',  # Assign device IDs
                    'source_row': idx
                }
                
                scoring_rows.append(scoring_row)
            except Exception as e:
                logger.debug(f"Error processing row {idx}: {e}")
                continue
        
        return scoring_rows
    
    def process_upload(self, filepath: str) -> Dict[str, Any]:
        """Process uploaded file and return scoring-ready data."""
        try:
            # Detect format
            format_type = self.detect_format(filepath)
            logger.info(f"Detected dataset format: {format_type}")
            
            # Load dataset
            df = self.load_dataset(filepath)
            if df is None or df.empty:
                return {'success': False, 'error': 'Failed to load dataset'}
            
            logger.info(f"Loaded dataset with shape: {df.shape}")
            
            # Normalize columns
            df = self.normalize_columns(df, format_type)
            
            # Clean data
            df = self.clean_data(df)
            
            # Extract scoring rows
            scoring_rows = self.extract_scoring_rows(df)
            
            if not scoring_rows:
                return {'success': False, 'error': 'No valid rows found for scoring'}
            
            return {
                'success': True,
                'format': format_type,
                'total_rows': len(df),
                'valid_rows': len(scoring_rows),
                'scoring_rows': scoring_rows,
                'filepath': filepath
            }
        except Exception as e:
            logger.error(f"Processing error: {e}", exc_info=True)
            return {'success': False, 'error': str(e)}
    
    def get_upload_stats(self) -> Dict[str, Any]:
        """Get statistics about uploaded datasets."""
        uploads = list(self.upload_dir.glob('*'))
        processed = list(self.processed_dir.glob('*'))
        
        return {
            'uploads_count': len(uploads),
            'processed_count': len(processed),
            'total_size_mb': sum(f.stat().st_size for f in uploads) / (1024 * 1024)
        }


# Global instance
_processor_instance = None

def get_processor() -> DatasetProcessor:
    """Get or create dataset processor instance."""
    global _processor_instance
    if _processor_instance is None:
        _processor_instance = DatasetProcessor()
    return _processor_instance

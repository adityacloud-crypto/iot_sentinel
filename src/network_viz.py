"""
IoT Sentinel - Network Visualization
Generates network topology and device relationship data for visualization.
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import random
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class NetworkNode:
    """Represents a device node in the network."""
    id: str
    type: str = 'device'
    status: str = 'normal'  # normal, suspicious, risky, anomaly
    trust_score: float = 100.0
    events_count: int = 0
    anomalies_count: int = 0
    ip_address: str = ''
    position: Dict[str, float] = None
    
    def to_dict(self):
        return asdict(self)


@dataclass
class NetworkLink:
    """Represents a connection between devices."""
    source: str
    target: str
    weight: float = 1.0
    protocol: str = 'TCP'
    bytes_transferred: int = 0
    
    def to_dict(self):
        return asdict(self)


class NetworkGraph:
    """Manages network topology and device relationships."""
    
    def __init__(self):
        self.nodes: Dict[str, NetworkNode] = {}
        self.links: List[NetworkLink] = []
        self.device_connections = defaultdict(lambda: defaultdict(int))
        
        # Network center for layout
        self.center_x = 500
        self.center_y = 300
        self.radius = 250
    
    def add_or_update_node(self, device_id: str, trust_score: float, 
                           verdict: str, event_data: Dict[str, Any] = None) -> NetworkNode:
        """Add or update a device node."""
        status_map = {
            'NORMAL': 'normal',
            'SUSPICIOUS': 'suspicious',
            'RISKY': 'risky',
            'ANOMALY': 'anomaly'
        }
        
        status = status_map.get(verdict.upper(), 'normal')
        
        if device_id in self.nodes:
            # Update existing node
            node = self.nodes[device_id]
            node.trust_score = trust_score
            node.status = status
            node.events_count += 1
            if event_data:
                node.anomalies_count += 1 if event_data.get('is_anomaly', False) else 0
        else:
            # Create new node with position
            position = self._calculate_position(len(self.nodes))
            
            # Generate pseudo IP address
            ip_parts = [192, 168, random.randint(1, 10), random.randint(1, 254)]
            ip_address = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.{ip_parts[3]}"
            
            node = NetworkNode(
                id=device_id,
                type='device',
                status=status,
                trust_score=trust_score,
                events_count=1,
                anomalies_count=1 if event_data and event_data.get('is_anomaly', False) else 0,
                ip_address=ip_address,
                position=position
            )
        
        self.nodes[device_id] = node
        
        # Create link to gateway/center
        if len(self.nodes) > 1:
            self._create_link(device_id)
        
        return node
    
    def _calculate_position(self, index: int) -> Dict[str, float]:
        """Calculate node position in circular layout."""
        if index == 0:
            # First node is the gateway at center
            return {'x': self.center_x, 'y': self.center_y}
        
        # Arrange other nodes in a circle
        angle = (2 * math.pi * index) / max(20, len(self.nodes))
        x = self.center_x + self.radius * math.cos(angle)
        y = self.center_y + self.radius * math.sin(angle)
        
        return {'x': x, 'y': y}
    
    def _create_link(self, device_id: str):
        """Create network link for device."""
        # Connect to gateway (first node)
        node_ids = list(self.nodes.keys())
        if len(node_ids) > 1:
            gateway_id = node_ids[0]
            if device_id != gateway_id:
                link = NetworkLink(
                    source=gateway_id,
                    target=device_id,
                    weight=1.0,
                    protocol='TCP',
                    bytes_transferred=0
                )
                self.links.append(link)
    
    def update_link_stats(self, source: str, target: str, 
                          bytes_count: int, protocol: str = 'TCP'):
        """Update link statistics."""
        for link in self.links:
            if (link.source == source and link.target == target) or \
               (link.source == target and link.target == source):
                link.bytes_transferred += bytes_count
                link.protocol = protocol
                link.weight = min(10, link.weight + 0.1)
                return
        
        # Create new link if not found
        new_link = NetworkLink(
            source=source,
            target=target,
            weight=1.0,
            protocol=protocol,
            bytes_transferred=bytes_count
        )
        self.links.append(new_link)
    
    def get_network_data(self) -> Dict[str, Any]:
        """Get network data for frontend visualization."""
        nodes_data = []
        for node in self.nodes.values():
            node_dict = node.to_dict()
            # Adjust position for frontend canvas
            if node_dict['position']:
                node_dict['position'] = {
                    'x': node_dict['position']['x'] % 800,
                    'y': node_dict['position']['y'] % 400
                }
            nodes_data.append(node_dict)
        
        links_data = [link.to_dict() for link in self.links]
        
        # Calculate network statistics
        total_nodes = len(self.nodes)
        total_links = len(self.links)
        anomaly_nodes = sum(1 for n in self.nodes.values() if n.status == 'anomaly')
        risky_nodes = sum(1 for n in self.nodes.values() if n.status == 'risky')
        suspicious_nodes = sum(1 for n in self.nodes.values() if n.status == 'suspicious')
        normal_nodes = sum(1 for n in self.nodes.values() if n.status == 'normal')
        
        avg_trust = sum(n.trust_score for n in self.nodes.values()) / max(1, total_nodes)
        
        return {
            'nodes': nodes_data,
            'links': links_data,
            'stats': {
                'total_devices': total_nodes,
                'total_connections': total_links,
                'anomaly_count': anomaly_nodes,
                'risky_count': risky_nodes,
                'suspicious_count': suspicious_nodes,
                'normal_count': normal_nodes,
                'avg_trust_score': round(avg_trust, 2),
                'network_health': self._calculate_network_health()
            }
        }
    
    def _calculate_network_health(self) -> float:
        """Calculate overall network health score (0-100)."""
        if not self.nodes:
            return 100.0
        
        # Weight factors
        weights = {
            'normal': 1.0,
            'suspicious': 0.7,
            'risky': 0.4,
            'anomaly': 0.1
        }
        
        total_weight = sum(
            weights.get(node.status, 1.0) * node.trust_score
            for node in self.nodes.values()
        )
        
        health = total_weight / len(self.nodes)
        return round(min(100, max(0, health)), 2)
    
    def get_device_details(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific device."""
        if device_id not in self.nodes:
            return None
        
        node = self.nodes[device_id]
        
        # Find connected devices
        connections = []
        for link in self.links:
            if link.source == device_id:
                connections.append({
                    'target': link.target,
                    'protocol': link.protocol,
                    'bytes': link.bytes_transferred,
                    'weight': link.weight
                })
            elif link.target == device_id:
                connections.append({
                    'source': link.source,
                    'protocol': link.protocol,
                    'bytes': link.bytes_transferred,
                    'weight': link.weight
                })
        
        return {
            **node.to_dict(),
            'connections': connections,
            'risk_level': self._get_device_risk_level(node)
        }
    
    def _get_device_risk_level(self, node: NetworkNode) -> str:
        """Determine device risk level."""
        if node.status == 'anomaly':
            return 'critical'
        elif node.status == 'risky':
            return 'high'
        elif node.status == 'suspicious':
            return 'medium'
        else:
            return 'low'
    
    def get_threat_intelligence(self) -> Dict[str, Any]:
        """Get threat intelligence summary."""
        threats = []
        
        for node in self.nodes.values():
            if node.status in ['anomaly', 'risky', 'suspicious']:
                threat = {
                    'device_id': node.id,
                    'status': node.status,
                    'trust_score': node.trust_score,
                    'anomalies': node.anomalies_count,
                    'risk_level': self._get_device_risk_level(node),
                    'ip_address': node.ip_address
                }
                threats.append(threat)
        
        # Sort by risk
        threats.sort(key=lambda x: x['trust_score'])
        
        return {
            'active_threats': len(threats),
            'critical_threats': sum(1 for t in threats if t['risk_level'] == 'critical'),
            'high_risk_threats': sum(1 for t in threats if t['risk_level'] == 'high'),
            'threats': threats[:20]  # Top 20 threats
        }
    
    def reset(self):
        """Reset the network graph."""
        self.nodes.clear()
        self.links.clear()
        self.device_connections.clear()


# Global instance
_network_graph = None

def get_network_graph() -> NetworkGraph:
    """Get or create network graph instance."""
    global _network_graph
    if _network_graph is None:
        _network_graph = NetworkGraph()
    return _network_graph

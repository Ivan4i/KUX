"""Health Monitor - monitors device health and sends alerts"""

from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger


class HealthMonitor:
    """Monitors device health and sends alerts"""

    def __init__(self):
        """Initialize Health Monitor"""
        self.alert_thresholds = {
            'battery_low': 15,  # percentage
            'temperature_high': 40,  # celsius
            'offline_timeout': 600,  # seconds (10 minutes)
        }
        self.last_alerts: Dict[str, datetime] = {}

    def check_device_health(self, device_status: Dict) -> List[Dict]:
        """
        Check device health and return alerts if needed

        Args:
            device_status: Device status dict from Device.get_status()

        Returns:
            list: List of alert dicts
        """
        alerts = []
        device_id = device_status['id']
        device_name = device_status['name']

        # Check battery level
        battery = device_status.get('battery_level', 0)
        if battery < self.alert_thresholds['battery_low'] and battery > 0:
            if self._should_send_alert(device_id, 'battery'):
                alerts.append({
                    'type': 'battery_low',
                    'level': 'warning',
                    'device_id': device_id,
                    'device_name': device_name,
                    'message': f"🔋 {device_name} has low battery: {battery}%",
                    'data': {'battery_level': battery}
                })
                self._mark_alert_sent(device_id, 'battery')

        # Check temperature
        temperature = device_status.get('temperature', 0)
        if temperature > self.alert_thresholds['temperature_high']:
            if self._should_send_alert(device_id, 'temperature'):
                alerts.append({
                    'type': 'temperature_high',
                    'level': 'warning',
                    'device_id': device_id,
                    'device_name': device_name,
                    'message': f"🔥 {device_name} is overheating: {temperature}°C",
                    'data': {'temperature': temperature}
                })
                self._mark_alert_sent(device_id, 'temperature')

        # Check offline status
        if device_status['current_status'] == 'offline':
            last_heartbeat = device_status.get('last_heartbeat')
            if last_heartbeat:
                # Check if offline for more than threshold
                # TODO: Implement offline timeout check
                pass

        return alerts

    def _should_send_alert(self, device_id: str, alert_type: str) -> bool:
        """
        Check if alert should be sent (avoid spam)

        Args:
            device_id: Device identifier
            alert_type: Type of alert

        Returns:
            bool: True if alert should be sent
        """
        alert_key = f"{device_id}:{alert_type}"
        last_alert = self.last_alerts.get(alert_key)

        if not last_alert:
            return True

        # Send alert again after 30 minutes
        time_since_last = (datetime.utcnow() - last_alert).total_seconds()
        return time_since_last > 1800

    def _mark_alert_sent(self, device_id: str, alert_type: str):
        """Mark that an alert was sent"""
        alert_key = f"{device_id}:{alert_type}"
        self.last_alerts[alert_key] = datetime.utcnow()


# Global HealthMonitor instance
health_monitor = HealthMonitor()

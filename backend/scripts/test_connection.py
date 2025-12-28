"""Test ADB connection to Pixel devices"""

import sys
from pathlib import Path
import yaml

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import get_settings


def test_adb_connection():
    """Test connection to all configured Pixel devices"""
    print("🔧 Testing ADB connections to Pixel devices...\n")

    settings = get_settings()

    # Load device configuration
    config_path = Path(__file__).parent.parent.parent / settings.device_config_path
    print(f"📁 Loading device config from: {config_path}")

    if not config_path.exists():
        print(f"❌ Device config file not found: {config_path}")
        return False

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    devices = config.get('devices', [])
    print(f"📱 Found {len(devices)} devices in config\n")

    all_success = True

    for device in devices:
        device_id = device['id']
        device_name = device['name']
        tailscale_ip = device['tailscale_ip']
        adb_port = device['adb_port']

        print(f"Testing {device_name} ({device_id})...")
        print(f"  IP: {tailscale_ip}:{adb_port}")

        # TODO: Implement actual ADB connection test
        # For now, just print info
        print(f"  ⚠️  ADB connection test not implemented yet")
        print(f"  ℹ️  To test manually: adb connect {tailscale_ip}:{adb_port}\n")

    if all_success:
        print("✅ All device configurations loaded successfully")
        print("\n📝 Note: Actual ADB connection testing will be implemented in Device Manager")
    else:
        print("❌ Some devices failed connection test")

    return all_success


if __name__ == "__main__":
    try:
        success = test_adb_connection()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error testing connections: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

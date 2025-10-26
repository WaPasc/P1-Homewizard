import os
from typing import Optional, Any
import requests
from dotenv import load_dotenv

load_dotenv()

HOMEWIZARD_IP = os.getenv('HOMEWIZARD_IP')
HOMEWIZARD_TOKEN = os.getenv('HOMEWIZARD_TOKEN')

INFLUXDB_TOKEN = os.getenv('INFLUXDB_ADMIN_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')

def fetch_homewizard_data() -> Optional[dict[str, Any]]:
    """Fetches latest measurements from homewizard device."""
    try:
        url = f"https://{HOMEWIZARD_IP}/api/measurement"
        headers = {
            "Authorization": f"Bearer {HOMEWIZARD_TOKEN}",
            "X-Api-Version": "2"
        }
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        response.raise_for_status()
        print(f"Succesfully fetched data: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def write_to_influxdb(data: dict[str, Any]):
    """Writes the fetched data into the InfluxDB bucket"""
    if not data:
        print("No data to write")
        return

if __name__ == "__main__":
    fetch_homewizard_data()

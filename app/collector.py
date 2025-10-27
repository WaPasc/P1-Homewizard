import os
import asyncio
import signal
import sys
import time
from typing import Optional, Any
import requests
from dotenv import load_dotenv
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

HOMEWIZARD_IP = os.getenv("HOMEWIZARD_IP")
HOMEWIZARD_TOKEN = os.getenv("HOMEWIZARD_TOKEN")

INFLUXDB_TOKEN = os.getenv("INFLUXDB_ADMIN_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")
INFLUXDB_URL = os.getenv("INFLUXDB_URL")

try:
    client = influxdb_client.InfluxDBClient(
        url=INFLUXDB_URL,
        token=INFLUXDB_TOKEN,
        org=INFLUXDB_ORG,
    )
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print(f"InfluxDB client initialized ({INFLUXDB_URL})")
except Exception as e:
    print(f"Failed to initialize InfluxDB client: {e}")
    exit(1)


def fetch_homewizard_data() -> Optional[dict[str, Any]]:
    try:
        url = f"https://{HOMEWIZARD_IP}/api/measurement"
        headers = {
            "Authorization": f"Bearer {HOMEWIZARD_TOKEN}",
            "X-Api-Version": "2",
        }
        response = requests.get(url, headers=headers, verify=False, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"Data fetched: {data}")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def write_to_influxdb(data: dict[str, Any]):
    if not data:
        print("No data to write.")
        return
    try:
        p = influxdb_client.Point("energy_metrics").time(time.time_ns())

        for key, value in data.items():
            try:
                p = p.field(key, float(value))
            except (ValueError, TypeError):
                continue

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=p)
        print(f"Wrote data to InfluxDB: {data}")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

async def main():
    while True:
        data = fetch_homewizard_data()
        write_to_influxdb(data)
        await asyncio.sleep(5) # Non-blocking sleep

def handle_exit(sig, frame):
    print("Stopping collector gracefully...")
    sys.exit(0)


signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

if __name__ == "__main__":
    asyncio.run(main())

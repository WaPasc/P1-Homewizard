import os
from typing import Optional, Any
import requests
from dotenv import load_dotenv

load_dotenv()

HOMEWIZARD_IP = os.getenv('HOMEWIZARD_IP')
HOMEWIZARD_TOKEN = os.getenv('HOMEWIZARD_TOKEN')

def fetch_homewizard_data() -> Optional[dict[str, Any]]:
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

if __name__ == "__main__":
    fetch_homewizard_data()

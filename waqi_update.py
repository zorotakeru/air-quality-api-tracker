import requests
import pandas as pd
import os
from datetime import datetime

# Get token from GitHub Secret
TOKEN = os.getenv('WAQI_TOKEN')
# Indonesia Map Bounds
BOUNDS = "-11.0,95.0,6.0,141.0"
FILE_NAME = "indonesia_aqi_dynamic.csv"

def fetch_data():
    url = f"https://api.waqi.info/map/bounds/?latlng={BOUNDS}&token={TOKEN}"
    try:
        r = requests.get(url).json()
        if r['status'] == 'ok':
            rows = []
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for s in r['data']:
                if s.get('aqi') != '-':
                    rows.append({
                        'Timestamp': now,
                        'Station': s.get('station', {}).get('name'),
                        'AQI': int(s.get('aqi')),
                        'Lat': s.get('lat'),
                        'Lon': s.get('lon')
                    })
            return pd.DataFrame(rows)
    except Exception as e:
        print(f"Error: {e}")
    return None

if __name__ == "__main__":
    new_data = fetch_data()
    if new_data is not None:
        if os.path.exists(FILE_NAME):
            # Append without header
            new_data.to_csv(FILE_NAME, mode='a', header=False, index=False)
        else:
            # Create new with header
            new_data.to_csv(FILE_NAME, index=False)
        print("Data successfully updated.")




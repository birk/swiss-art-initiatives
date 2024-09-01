import pandas as pd
import requests
import time

# Script used once to retrieve WGS84 geodata from Nominatim API for data/places.csv based of the given address.

# Read the CSV file
df = pd.read_csv('data/places.csv', dtype=str)
df.fillna("", inplace=True)

# Function to get WGS84 geodata using Nominatim API


def get_WGS84(row):
    print(row['id'])

    # Skip lines with missing address or post code
    if row['address'] != "" and row['post_code'] != "":
        url = 'https://nominatim.openstreetmap.org/search.php'
        params = {
            'street': row['address'],
            'postalcode': row['post_code'],
            'city': row['city'],
            'country': 'Switzerland',
            'polygon_geojson': '1',
            'format': 'jsonv2'
        }
        headers = {
            "User-Agent": "HSLU/1.0 (+https://hslu.ch)",
            "Referer": "https://hslu.ch"
        }
        time.sleep(1)
        try:
            response = requests.get(
                url, params=params, headers=headers, timeout=10)
            if response.status_code == 200 and len(response.json()) > 0:
                return pd.Series({'lat': response.json()[0]['lat'], 'lon': response.json()[0]['lon']})
            else:
                print(
                    f"API returned {response.status_code} status code and found {len(response.json())} results.")
                return pd.Series({'lat': '', 'lon': ''})
        except Exception as e:
            print(f"Error occurred: {e}")
            return pd.Series({'lat': '', 'lon': ''})
    return pd.Series({'lat': '', 'lon': ''})


# Apply the function to each row in the CSV with a progress bar
df[['WGS84_lat', 'WGS84_lon']] = df.apply(get_WGS84, axis=1)

# Reorder the columns
pos_y_index = df.columns.get_loc('pos_y')
cols = list(df.columns)
cols.insert(pos_y_index + 1, 'WGS84_lat')
cols.insert(pos_y_index + 2, 'WGS84_lon')
df = df[cols]
num_cols = df.shape[1]
df = df.iloc[:, :num_cols-2]

# Save the updated CSV with WGS84
df.to_csv('data/places_with_WGS84.csv', lineterminator='\n', index=False)

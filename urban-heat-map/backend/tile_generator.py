import os
import requests
import mercantile
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image
import numpy as np
import json

TEMP_CACHE_FILE = "cache/temp_cache.json"
WIND_CACHE_FILE = "cache/wind_cache.json"

# Load or initialize caches
def load_cache(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}

TEMP_CACHE = load_cache(TEMP_CACHE_FILE)
WIND_CACHE = load_cache(WIND_CACHE_FILE)

SAMPLES_BY_ZOOM = {5: 16}

# Common bounds
US_BOUNDS = {
    "lat_min": 24.396308,
    "lat_max": 49.384358,
    "lon_min": -125.0,
    "lon_max": -66.93457
}

GLOBAL_TEMP_MIN = 10
GLOBAL_TEMP_MAX = 40

GLOBAL_WIND_MIN = 0
GLOBAL_WIND_MAX = 30  # Adjust based on data

def fetch_point_temp(lat, lon):
    key = f"{round(lat, 4)},{round(lon, 4)}"
    if key in TEMP_CACHE:
        return TEMP_CACHE[key]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        temp = data.get("current_weather", {}).get("temperature")
    except Exception as e:
        print(f"⚠️ Failed to fetch temp for {lat},{lon}: {e}")
        temp = None

    TEMP_CACHE[key] = temp
    with open(TEMP_CACHE_FILE, "w") as f:
        json.dump(TEMP_CACHE, f)
    return temp

def fetch_point_wind(lat, lon):
    key = f"{round(lat, 4)},{round(lon, 4)}"
    if key in WIND_CACHE:
        return WIND_CACHE[key]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        wind = data.get("current_weather", {}).get("windspeed")
    except Exception as e:
        print(f"⚠️ Failed to fetch wind for {lat},{lon}: {e}")
        wind = None

    WIND_CACHE[key] = wind
    with open(WIND_CACHE_FILE, "w") as f:
        json.dump(WIND_CACHE, f)
    return wind

def generate_tile(z, x, y, layer_type='temperature', samples=None):
    if samples is None:
        samples = SAMPLES_BY_ZOOM.get(z, 8)

    tile_path = f"cache/tiles/{layer_type}/{z}/{x}/{y}.png"
    if os.path.exists(tile_path):
        return tile_path

    os.makedirs(os.path.dirname(tile_path), exist_ok=True)

    bounds = mercantile.bounds(x, y, z)

    if (bounds.north < US_BOUNDS["lat_min"] or bounds.south > US_BOUNDS["lat_max"] or
        bounds.east < US_BOUNDS["lon_min"] or bounds.west > US_BOUNDS["lon_max"]):
        print(f"Skipping tile z={z} x={x} y={y} — outside U.S.")
        return None

    lats = np.linspace(bounds.south, bounds.north, samples)
    lons = np.linspace(bounds.west, bounds.east, samples)

    data = np.empty((samples, samples))
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            if layer_type == 'temperature':
                value = fetch_point_temp(lat, lon)
            elif layer_type == 'wind':
                value = fetch_point_wind(lat, lon)
            else:
                raise ValueError(f"Unknown layer_type: {layer_type}")
            data[i, j] = value if value is not None else np.nan

    fig, ax = plt.subplots(figsize=(1, 1), dpi=256)

    if layer_type == 'temperature':
        cmap = "inferno"
        vmin, vmax = GLOBAL_TEMP_MIN, GLOBAL_TEMP_MAX
    else:
        cmap = "Blues"
        vmin, vmax = GLOBAL_WIND_MIN, GLOBAL_WIND_MAX

    ax.imshow(data, cmap=cmap, origin="lower", interpolation="bicubic", vmin=vmin, vmax=vmax)
    ax.axis('off')
    plt.subplots_adjust(0, 0, 1, 1)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)
    img.save(tile_path)

    return tile_path

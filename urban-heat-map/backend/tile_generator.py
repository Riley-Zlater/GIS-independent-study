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

CACHE_FILE = "cache/temp_cache.json"

# Load or initialize cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        TEMP_CACHE = json.load(f)
else:
    TEMP_CACHE = {}

# Zoom level → number of lat/lon samples per tile
SAMPLES_BY_ZOOM = {5: 16, 6: 32}

GLOBAL_MIN = 10
GLOBAL_MAX = 40


def fetch_point_temp(lat, lon):
    key = f"{round(lat, 4)},{round(lon, 4)}"

    # Check cache
    if key in TEMP_CACHE:
        return TEMP_CACHE[key]

    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        res = requests.get(url, timeout=5)
        data = res.json()
        temp = data.get("current_weather", {}).get("temperature")
    except Exception as e:
        print(f"⚠️ Failed to fetch temperature for {lat},{lon}: {e}")
        temp = None

    # Cache the result
    TEMP_CACHE[key] = temp
    with open(CACHE_FILE, "w") as f:
        json.dump(TEMP_CACHE, f)

    return temp

def generate_tile(z, x, y, samples=None):
    if samples is None:
        samples = SAMPLES_BY_ZOOM.get(z, 8)

    tile_path = f"cache/tiles/{z}/{x}/{y}.png"
    if os.path.exists(tile_path):
        return tile_path

    os.makedirs(os.path.dirname(tile_path), exist_ok=True)

    bounds = mercantile.bounds(x, y, z)
    lats = np.linspace(bounds.south, bounds.north, samples)
    lons = np.linspace(bounds.west, bounds.east, samples)

    temps = np.empty((samples, samples))
    for i, lat in enumerate(lats):
        for j, lon in enumerate(lons):
            temp = fetch_point_temp(lat, lon)
            temps[i, j] = temp if temp is not None else np.nan

    fig, ax = plt.subplots(figsize=(1, 1), dpi=256)
    ax.imshow(temps, cmap="inferno", origin="lower", interpolation="bicubic", vmin=GLOBAL_MIN, vmax=GLOBAL_MAX)
    ax.axis('off')
    plt.subplots_adjust(0, 0, 1, 1)

    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)
    img.save(tile_path)

    return tile_path

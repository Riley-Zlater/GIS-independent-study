from matplotlib import cm
from PIL import Image
import numpy as np
import os
import mercantile
import pyproj
from weather_data import fetch_point_temp

SAMPLES_BY_ZOOM = {
    4: 8,
    5: 16,
    6: 32,
    7: 64,
}
GLOBAL_TEMP_MIN = 10
GLOBAL_TEMP_MAX = 40

to_latlon = pyproj.Transformer.from_crs("EPSG:3857", "EPSG:4326", always_xy=True)
to_webmerc = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)

def generate_tile(z, x, y, layer_type='temperature', samples=None):
    if samples is None:
        samples = SAMPLES_BY_ZOOM.get(z, 8)

    tile_path = f"cache/tiles/{layer_type}/{z}/{x}/{y}.png"
    if os.path.exists(tile_path):
        return tile_path

    os.makedirs(os.path.dirname(tile_path), exist_ok=True)

    bounds = mercantile.bounds(x, y, z)
    left, bottom = to_webmerc.transform(bounds.west, bounds.south)
    right, top = to_webmerc.transform(bounds.east, bounds.north)

    xs = np.linspace(left, right, samples)
    ys = np.linspace(top, bottom, samples)

    X, Y = np.meshgrid(xs, ys)
    lon, lat = to_latlon.transform(X, Y)

    data = np.empty((samples, samples))
    for i in range(samples):
        for j in range(samples):
            value = fetch_point_temp(lat[i, j], lon[i, j])
            data[i, j] = value if value is not None else np.nan

    norm = (data - GLOBAL_TEMP_MIN) / (GLOBAL_TEMP_MAX - GLOBAL_TEMP_MIN)
    norm = np.clip(norm, 0, 1)
    rgba = cm.inferno(norm)

    img = Image.fromarray((rgba[:, :, :3] * 255).astype(np.uint8))
    img = img.resize((256, 256), resample=Image.BICUBIC)
    img.save(tile_path)

    return tile_path

import xarray as xr
import numpy as np

print("⏳ Loading GRIB2 temperature data...")
ds = xr.open_dataset("gdas.t18z.pgrb2.0p25.f000", engine="cfgrib", filter_by_keys={"typeOfLevel": "surface"})
print("✅ Loaded GRIB2 data.")
# print(ds)

# Extract data
temps = ds['t'].values         # Temperature data in Kelvin
lats = ds.latitude.values      # Shape: (721,)
lons = ds.longitude.values     # Shape: (1440,)

# Flip latitudes if descending
if lats[0] > lats[-1]:
    lats = lats[::-1]
    temps = temps[::-1, :]  # Flip latitude dimension to match

def fetch_point_temp(lat, lon):
    """Interpolated temperature using xarray's native grid-aware method."""
    if lon < 0:
        lon += 360

    try:
        result = ds['t'].interp(latitude=lat, longitude=lon, method="linear")
        return float(result.values) - 273.15
    except Exception:
        return np.nan


# print(fetch_point_temp(35.0, -97.0))  # Test point

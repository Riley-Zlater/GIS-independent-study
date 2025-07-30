from tile_generator import generate_tile
import mercantile

# United States bounding box (approximate)
US_LAT_MIN = 24.396308
US_LAT_MAX = 49.384358
US_LON_MIN = -125.0
US_LON_MAX = -66.93457

LAYER_TYPES = ["temperature", "wind"]
ZOOM = 5  # Fixed zoom level

def tile_in_us(bounds):
    return (
        bounds.south < US_LAT_MAX and bounds.north > US_LAT_MIN and
        bounds.west < US_LON_MAX and bounds.east > US_LON_MIN
    )

def precompute_tiles():
    total = 0
    for x in range(2**ZOOM):
        for y in range(2**ZOOM):
            bounds = mercantile.bounds(x, y, ZOOM)
            if tile_in_us(bounds):
                for layer in LAYER_TYPES:
                    print(f"Generating {layer} tile z={ZOOM} x={x} y={y}")
                    try:
                        path = generate_tile(ZOOM, x, y, layer_type=layer)
                        print(f"Saved to {path}")
                        total += 1
                    except Exception as e:
                        print(f"⚠️ Failed to generate {layer} tile z={ZOOM} x={x} y={y}: {e}")
    print(f"✅ Done. Generated {total} tiles at zoom {ZOOM} for layers: {', '.join(LAYER_TYPES)}")

if __name__ == "__main__":
    precompute_tiles()

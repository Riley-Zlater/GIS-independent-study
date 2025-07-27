from tile_generator import generate_tile
import mercantile

# United States bounding box (approximate)
US_LAT_MIN = 24.396308
US_LAT_MAX = 49.384358
US_LON_MIN = -125.0
US_LON_MAX = -66.93457

def tile_in_us(bounds):
    return (
        bounds.south < US_LAT_MAX and bounds.north > US_LAT_MIN and
        bounds.west < US_LON_MAX and bounds.east > US_LON_MIN
    )

def precompute_tiles(min_zoom=2, max_zoom=5):
    total = 0
    for zoom in range(min_zoom, max_zoom + 1):
        for x in range(2**zoom):
            for y in range(2**zoom):
                bounds = mercantile.bounds(x, y, zoom)
                if tile_in_us(bounds):
                    print(f"Generating tile z={zoom} x={x} y={y}")
                    path = generate_tile(zoom, x, y)
                    print(f"Saved to {path}")
                    total += 1
    print(f"✅ Done. Generated {total} US tiles from zoom {min_zoom} to {max_zoom}.")

if __name__ == "__main__":
    precompute_tiles(min_zoom=2, max_zoom=5)

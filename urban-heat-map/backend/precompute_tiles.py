from tile_generator import generate_tile
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

LAYER_TYPES = ["temperature"]
ZOOM_LEVELS = [4, 5, 6, 7]
MAX_WORKERS = 16


def tile_tasks():
    for z in ZOOM_LEVELS:
        num_tiles = 2 ** z
        for x in range(num_tiles):
            for y in range(num_tiles):
                for layer in LAYER_TYPES:
                    yield (z, x, y, layer)


def generate_task(args):
    z, x, y, layer = args
    try:
        path = generate_tile(z, x, y, layer_type=layer)
        if path:
            return True
        else:
            return False
    except Exception as e:
        print(f"⚠️ Failed to generate {layer} tile z={z} x={x} y={y}: {e}")
        return False


def precompute_tiles():
    total = 0
    tasks = list(tile_tasks())

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(generate_task, task) for task in tasks]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Generating tiles"):
            if future.result():
                total += 1

    print(f"\n✅ Done. Generated {total} tile(s) at zooms {ZOOM_LEVELS} for layers: {', '.join(LAYER_TYPES)}")


if __name__ == "__main__":
    precompute_tiles()

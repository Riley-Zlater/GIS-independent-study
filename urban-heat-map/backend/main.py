from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import os

from tile_generator import generate_tile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tiles/{layer}/{z}/{x}/{y}.png")
async def serve_tile(layer: str, z: int, x: int, y: int):
    print(f"Tile requested: layer={layer}, z={z}, x={x}, y={y}")
    
    if layer not in ("temperature", "wind"):
        return Response(content="Invalid layer type", status_code=400)
    
    tile_path = f"cache/tiles/{layer}/{z}/{x}/{y}.png"

    if not os.path.exists(tile_path):
        try:
            generate_tile(z, x, y, layer_type=layer)
        except Exception as e:
            return Response(content=f"Tile generation failed: {e}", status_code=500)

    if os.path.exists(tile_path):
        with open(tile_path, "rb") as f:
            return Response(content=f.read(), media_type="image/png")
    else:
        return Response(content="Tile not found", status_code=404)

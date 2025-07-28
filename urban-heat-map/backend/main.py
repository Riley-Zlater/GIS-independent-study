# backend/main.py
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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

@app.get("/tiles/{z}/{x}/{y}.png")
async def serve_tile(z: int, x: int, y: int):
    print(f"Tile requested: z={z}, x={x}, y={y}")
    tile_path = f"cache/tiles/{z}/{x}/{y}.png"
    if not os.path.exists(tile_path):
        try:
            generate_tile(z, x, y)
        except Exception as e:
            return Response(content=f"Tile generation failed: {e}", status_code=500)
    if os.path.exists(tile_path):
        with open(tile_path, "rb") as f:
            return Response(content=f.read(), media_type="image/png")
    else:
        return Response(content="Tile not found", status_code=404)


app.mount("/static", StaticFiles(directory="cache/stitched"), name="static")
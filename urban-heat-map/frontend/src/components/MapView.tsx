import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const TILE_ROOT = "http://localhost:8000/tiles/"
const TILE_COORDS = "{z}/{x}/{y}.png";

const TEMP_TILE_URL = `${TILE_ROOT}temperature/${TILE_COORDS}`;
const WIND_TILE_URL = `${TILE_ROOT}wind/${TILE_COORDS}`;

const MapView: React.FC = () => {
    const [activeHeatmap, setActiveHeatmap] = useState<null | 'temperature' | 'wind'>(null);
    const mapRef = useRef<any>(null);

    const toggleHeatmap = (type: 'temperature' | 'wind') => {
        setActiveHeatmap(prev => (prev === type ? null : type));
    };

    const getHeatmapTileUrl = () => {
        if (activeHeatmap === 'temperature') return TEMP_TILE_URL;
        if (activeHeatmap === 'wind') return WIND_TILE_URL;
        return null;
    };

    return (
        <div style={{ height: "80vh", width: "100%" }}>
            <MapContainer
                center={[37.8, -96]}
                zoom={5}
                minZoom={5}
                maxZoom={5}
                style={{ height: "100%", width: "100%" }}
                maxBounds={[[49.384358, -125.0], [24.396308, -66.93457]]}
                whenCreated={mapInstance => { mapRef.current = mapInstance; }}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                />

                {activeHeatmap && (
                    <TileLayer
                        url={getHeatmapTileUrl()!}
                        tileSize={256}
                        opacity={0.5}
                        attribution={`${activeHeatmap === 'temperature' ? 'Urban Heat Map' : 'Wind Speed Map'}`}
                        noWrap={true}
                        crossOrigin="anonymous"
                        updateWhenIdle={true}
                        updateWhenZooming={false}
                        zIndex={500}
                    />
                )}
            </MapContainer>

            <div style={{ marginTop: 10 }}>
                <button onClick={() => toggleHeatmap('temperature')}>
                    {activeHeatmap === 'temperature' ? 'Hide Temperature Heat Map' : 'Show Temperature Heat Map'}
                </button>
                <button onClick={() => toggleHeatmap('wind')} style={{ marginLeft: 10 }}>
                    {activeHeatmap === 'wind' ? 'Hide Wind Speed Heat Map' : 'Show Wind Speed Heat Map'}
                </button>
            </div>
        </div>
    );
};

export default MapView;

import React, { useRef, useState } from 'react';
import { MapContainer, TileLayer } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';


const TILE_URL = "http://localhost:8000/tiles/{z}/{x}/{y}.png";

const MapView: React.FC = () => {
    const [showHeatmap, setShowHeatmap] = useState(false);
    const mapRef = useRef<any>(null);

    const handleGenerateHeatmap = () => {
        console.log("Toggle Heat Map clicked");
        setShowHeatmap(!showHeatmap);
    };

    return (
        <div style={{ height: "80vh", width: "100%" }}>
            <MapContainer
                center={[37.8, -96]} // Center of the US
                zoom={5}
                minZoom={5}
                maxZoom={5}
                style={{ height: "100%", width: "100%" }}
                maxBounds={[[49.384358, -125.0], [24.396308, -66.93457]]} // US bounding box
                whenCreated={mapInstance => { mapRef.current = mapInstance; }}
            >
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution="&copy; OpenStreetMap contributors"
                />
                {showHeatmap && (
                    <TileLayer
                        url={TILE_URL}
                        tileSize={256}
                        opacity={0.5}
                        attribution="Urban Heat Map"
                        noWrap={true}
                        crossOrigin="anonymous"
                        updateWhenIdle={true}
                        updateWhenZooming={false}
                        zIndex={500}
                    />
                )}
            </MapContainer>
            <button onClick={handleGenerateHeatmap} style={{marginTop: 10}}>
                {showHeatmap ? 'Hide Heat Map' : 'Show Heat Map'}
            </button>
        </div>
    );
};

export default MapView;
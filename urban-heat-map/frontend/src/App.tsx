import React from 'react';
import './styles/App.css';
import MapView from './components/MapView';

const App: React.FC = () => {
    return (
        <div className="App">
            <h1>Urban Heat Map</h1>
            <MapView />
        </div>
    );
};

export default App;
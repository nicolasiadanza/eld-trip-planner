import React, { useState } from 'react';
import TripForm from './components/TripForm/TripForm';
import MapView from './components/MapView/MapView';
import RouteInfo from './components/RouteInfo/RouteInfo';
import ELDLog from './components/ELDLog/ELDLog';
import Spinner from './components/common/Spinner';
import ErrorMessage from './components/common/ErrorMessage';
import { createTrip } from './services/api';
import './App.css';

const App = () => {
  const [tripData, setTripData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setTripData(null); // Clear previous trip data
    setIsLoading(true);
    setError(null);

    try {
      const result = await createTrip(formData);
      setTripData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚛 ELD Trip Planner</h1>
        <p>HOS Compliant Route Planning</p>
      </header>
      {isLoading && (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 'calc(100vh - 24px)' }}>
          <Spinner />
        </div>
      )}
      {!isLoading && error && <ErrorMessage message={error} />}
      {!isLoading && !error && (
        <div className="main-content">
          <div className="left-panel">
            <TripForm onSubmit={handleSubmit} isLoading={isLoading} />
          </div>
          {tripData && (
            <div className="right-panel">
              <MapView tripData={tripData} className="map-container" />
              <RouteInfo tripData={tripData} />
              <ELDLog tripData={tripData} />
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default App;

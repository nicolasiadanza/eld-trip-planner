import React, { useState } from 'react';
import './TripForm.css';

const TripForm = ({ onSubmit, isLoading }) => {
  const [currentLocation, setCurrentLocation] = useState('');
  const [pickupLocation, setPickupLocation] = useState('');
  const [dropoffLocation, setDropoffLocation] = useState('');
  const [currentCycleUsed, setCurrentCycleUsed] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      current_location: currentLocation,
      pickup_location: pickupLocation,
      dropoff_location: dropoffLocation,
      current_cycle_used: parseFloat(currentCycleUsed),
    });
  };

  return (
    <form className="trip-form" onSubmit={handleSubmit}>
      <h2>Trip Planner</h2>
      <div className="form-group">
        <label htmlFor="currentLocation">Current Location</label>
        <input
          type="text"
          id="currentLocation"
          placeholder="e.g. Chicago, IL"
          value={currentLocation}
          onChange={(e) => setCurrentLocation(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="pickupLocation">Pickup Location</label>
        <input
          type="text"
          id="pickupLocation"
          placeholder="e.g. Indianapolis, IN"
          value={pickupLocation}
          onChange={(e) => setPickupLocation(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="dropoffLocation">Dropoff Location</label>
        <input
          type="text"
          id="dropoffLocation"
          placeholder="e.g. Nashville, TN"
          value={dropoffLocation}
          onChange={(e) => setDropoffLocation(e.target.value)}
        />
      </div>
      <div className="form-group">
        <label htmlFor="currentCycleUsed">Current Cycle Used</label>
        <input
          type="number"
          id="currentCycleUsed"
          min="0"
          max="70"
          step="0.5"
          placeholder="e.g. 12.5"
          value={currentCycleUsed}
          onChange={(e) => setCurrentCycleUsed(e.target.value)}
        />
      </div>
      <button type="submit" disabled={isLoading} className="submit-btn">
        {isLoading ? 'Planning Trip...' : 'Plan My Trip 🚛'}
      </button>
    </form>
  );
};

export default TripForm;

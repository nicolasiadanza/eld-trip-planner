import React from 'react';
import PropTypes from 'prop-types';
import './RouteInfo.css';

const RouteInfo = ({ tripData }) => {
  if (!tripData) return null;

  const getStopIcon = (stopType) => {
    switch (stopType) {
      case 'driving':
        return '🚚';
      case 'pickup':
        return '📦';
      case 'dropoff':
        return '🏁';
      case 'rest_30min':
        return '☕';
      case 'rest_10hr':
        return '😴';
      case 'fuel':
        return '⛽';
      default:
        return '';
    }
  };

  const getStopColor = (stopType) => {
    switch (stopType) {
      case 'driving':
        return 'blue';
      case 'pickup':
      case 'dropoff':
        return 'purple';
      case 'rest_30min':
      case 'rest_10hr':
        return 'orange';
      case 'fuel':
        return 'green';
      default:
        return 'gray';
    }
  };

  const formatDuration = (hours) => {
    if (hours < 1) return `${Math.round(hours * 60)} min`;
    return `${hours.toFixed(1)} hrs`;
  };

  return (
    <div className="route-info">
      <div className="summary-section">
        <div className="stat-card">
          <h3>Total Distance</h3>
          <p>{tripData.total_distance_miles.toFixed(1)} miles</p>
        </div>
        <div className="stat-card">
          <h3>Total Duration</h3>
          <p>{tripData.total_duration_hours.toFixed(1)} hours</p>
        </div>
      </div>
      <ul className="stop-list">
        {tripData.stops.map((stop, index) => (
          <li key={index} className={`stop-item ${stop.stop_type}`}>
            <span className="icon">{getStopIcon(stop.stop_type)}</span>
            <span className="location-name">{stop.location_name}</span>
            <span className="arrival-time">
              {new Date(stop.arrival_time).toLocaleString()}
            </span>
            <span className="duration-hours">{formatDuration(stop.duration_hours)}</span>
            <span className="badge" style={{ backgroundColor: getStopColor(stop.stop_type) }}>
              {stop.stop_type}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

RouteInfo.propTypes = {
  tripData: PropTypes.object,
};

export default RouteInfo;

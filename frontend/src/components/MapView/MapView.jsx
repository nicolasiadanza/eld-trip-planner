import React from 'react';
import { MapContainer, TileLayer, Polyline, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// Fix leaflet default icon issue
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

const MapView = ({ tripData }) => {
  if (!tripData) return null;
  if (!tripData.route_geometry) return null;
  if (!tripData.route_geometry.coordinates) return null;
  if (tripData.route_geometry.coordinates.length === 0) return null;

  const routeCoordinates = tripData.route_geometry.coordinates.map(coord => [coord[1], coord[0]]);
  const mapCenter = routeCoordinates.length > 0 ? routeCoordinates[0] : [52.52, 13.405]; // Default to Berlin if no coordinates

  return (
    <MapContainer center={mapCenter} zoom={6} style={{ height: '400px' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      <Polyline positions={routeCoordinates} color="#2563eb" weight={4} />
      {tripData.stops.filter(stop => stop.lat !== 0 || stop.lng !== 0).map(stop => (
        <Marker key={stop.id} position={[stop.lat, stop.lng]}>
          <Popup>
            <div>
              <strong>{stop.stop_type}</strong><br />
              {stop.location_name}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapView;

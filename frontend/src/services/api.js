import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
})

export const createTrip = async (tripData) => {
  // Asegurarse de que los datos estén en snake_case
  const formattedTripData = {
    current_location: tripData.currentLocation,
    pickup_location: tripData.pickupLocation,
    dropoff_location: tripData.dropoffLocation,
    current_cycle_used: tripData.currentCycleUsed
  };

  const response = await api.post('/api/trips/', formattedTripData)
  return response.data
}

export const getTrip = async (id) => {
  const response = await api.get(`/api/trips/${id}/`)
  return response.data
}

export default api

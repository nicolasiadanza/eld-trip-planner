import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' }
})

export const createTrip = async (tripData) => {
  const response = await api.post('/api/trips/', tripData)
  return response.data
}

export const getTrip = async (id) => {
  const response = await api.get(`/api/trips/${id}/`)
  return response.data
}

export default api

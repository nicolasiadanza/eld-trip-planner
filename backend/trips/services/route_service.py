import requests
import time
from django.conf import settings

def geocode_location(location_name: str) -> dict:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location_name,
        'format': 'json',
        'limit': 1
    }
    headers = {'User-Agent': 'ELDTripPlanner/1.0'}
    
    response = requests.get(url, params=params, headers=headers)
    time.sleep(1)  # Respect Nominatim rate limit
    
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return {
            'lat': float(data['lat']),
            'lng': float(data['lon']),
            'display_name': data['display_name']
        }
    else:
        raise ValueError("Location not found")

def get_route(origin_lat, origin_lng, dest_lat, dest_lng) -> dict:
    url = f"http://router.project-osrm.org/route/v1/driving/{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
    params = {
        'overview': 'full',
        'geometries': 'geojson',
        'steps': 'false'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check that response JSON has "code" == "Ok" AND "routes" exists AND len(routes) > 0
        if data['code'] == 'Ok' and 'routes' in data and len(data['routes']) > 0:
            route = data['routes'][0]
            
            # Get distance from route["legs"][0]["distance"]
            distance_meters = route['legs'][0]['distance']
            
            # Get duration from route["legs"][0]["duration"]
            duration_seconds = route['legs'][0]['duration']
            
            # Get geometry from route["geometry"]
            geometry = route['geometry']
            
            # Convert distance from meters to miles
            distance_miles = distance_meters / 1609.34
            
            # Convert duration from seconds to hours
            duration_hours = duration_seconds / 3600
            
            return {
                'distance_miles': distance_miles,
                'duration_hours': duration_hours,
                'geometry': geometry
            }
        else:
            raise ValueError("Route not found")
    else:
        raise ValueError("Route not found")

def get_full_route(current_lat, current_lng, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng) -> dict:
    first_leg = get_route(current_lat, current_lng, pickup_lat, pickup_lng)
    second_leg = get_route(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
    
    combined_geometry = {
        "type": "LineString",
        "coordinates": first_leg['geometry']['coordinates'] + second_leg['geometry']['coordinates'][1:]
    }
    
    return {
        'total_distance_miles': first_leg['distance_miles'] + second_leg['distance_miles'],
        'total_duration_hours': first_leg['duration_hours'] + second_leg['duration_hours'],
        'geometry': combined_geometry
    }

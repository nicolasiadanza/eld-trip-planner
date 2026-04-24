from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import Trip, Stop, ELDLogSheet
from .serializers import TripSerializer, TripInputSerializer
from .services.route_service import geocode_location, get_full_route
from .services.hos_calculator import calculate_trip_plan
from .services.log_generator import generate_log_sheets

class TripCreateView(APIView):
    def post(self, request):
        serializer = TripInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Geocode locations
            current_location = geocode_location(serializer.validated_data['current_location'])
            pickup_location = geocode_location(serializer.validated_data['pickup_location'])
            dropoff_location = geocode_location(serializer.validated_data['dropoff_location'])

            # Get full route
            route_data = get_full_route(
                current_location['lat'], current_location['lng'],
                pickup_location['lat'], pickup_location['lng'],
                dropoff_location['lat'], dropoff_location['lng']
            )

            # Calculate trip plan
            stops_plan = calculate_trip_plan(
                route_data['total_distance_miles'],
                route_data['total_duration_hours'],
                serializer.validated_data['current_cycle_used'],
                serializer.validated_data['pickup_location'],
                serializer.validated_data['dropoff_location']
            )

            # Generate log sheets
            log_sheets = generate_log_sheets(stops_plan)

            # Create Trip object
            trip = Trip.objects.create(
                current_location=serializer.validated_data['current_location'],
                pickup_location=serializer.validated_data['pickup_location'],
                dropoff_location=serializer.validated_data['dropoff_location'],
                current_cycle_used=serializer.validated_data['current_cycle_used'],
                current_lat=current_location['lat'],
                current_lng=current_location['lng'],
                pickup_lat=pickup_location['lat'],
                pickup_lng=pickup_location['lng'],
                dropoff_lat=dropoff_location['lat'],
                dropoff_lng=dropoff_location['lng'],
                total_distance_miles=route_data['total_distance_miles'],
                total_duration_hours=route_data['total_duration_hours'],
                route_geometry=route_data['geometry']
            )

            # Create Stop objects
            for stop_data in stops_plan:
                Stop.objects.create(
                    trip=trip,
                    stop_type=stop_data['stop_type'],
                    location_name=stop_data['location_name'],
                    arrival_time=stop_data['arrival_time'],
                    departure_time=stop_data['departure_time'],
                    duration_hours=stop_data['duration_hours'],
                    order=stop_data['order'],
                    lat=stop_data['lat'],
                    lng=stop_data['lng']
                )

            # Create ELDLogSheet objects
            for log in log_sheets:
                ELDLogSheet.objects.create(
                    trip=trip,
                    day_number=log['day_number'],
                    date=log['date'],
                    log_data=log['log_data']
                )

            return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TripDetailView(APIView):
    def get(self, request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        return Response(TripSerializer(trip).data, status=status.HTTP_200_OK)


def health_check(request):
    return JsonResponse({'status': 'ok'})

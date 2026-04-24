from rest_framework import serializers
from .models import Trip, Stop, ELDLogSheet

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['id', 'stop_type', 'location_name', 'lat', 'lng', 'arrival_time', 'departure_time', 'duration_hours', 'order']

class ELDLogSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ELDLogSheet
        fields = ['id', 'day_number', 'date', 'log_data']

class TripSerializer(serializers.ModelSerializer):
    stops = StopSerializer(many=True, read_only=True)
    log_sheets = ELDLogSheetSerializer(many=True, read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'current_location', 'pickup_location', 'dropoff_location', 
            'current_cycle_used', 'current_lat', 'current_lng', 'pickup_lat', 
            'pickup_lng', 'dropoff_lat', 'dropoff_lng', 'total_distance_miles', 
            'total_duration_hours', 'route_geometry', 'created_at', 'stops', 'log_sheets'
        ]

class TripInputSerializer(serializers.Serializer):
    current_location = serializers.CharField()
    pickup_location = serializers.CharField()
    dropoff_location = serializers.CharField()
    current_cycle_used = serializers.FloatField(min_value=0, max_value=70)

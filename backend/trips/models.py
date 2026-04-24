from django.db import models

class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_cycle_used = models.FloatField()
    current_lat = models.FloatField(null=True)
    current_lng = models.FloatField(null=True)
    pickup_lat = models.FloatField(null=True)
    pickup_lng = models.FloatField(null=True)
    dropoff_lat = models.FloatField(null=True)
    dropoff_lng = models.FloatField(null=True)
    total_distance_miles = models.FloatField(null=True)
    total_duration_hours = models.FloatField(null=True)
    route_geometry = models.JSONField(null=True, blank=True)  # Nuevo campo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pickup_location} → {self.dropoff_location}"

class Stop(models.Model):
    STOP_TYPES = [
        ('driving', 'Driving'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('rest_30min', 'Rest 30min'),
        ('rest_10hr', 'Rest 10hr'),
        ('fuel', 'Fuel')
    ]
    trip = models.ForeignKey(Trip, related_name='stops', on_delete=models.CASCADE)
    stop_type = models.CharField(choices=STOP_TYPES, max_length=255)
    location_name = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()
    duration_hours = models.FloatField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

class ELDLogSheet(models.Model):
    trip = models.ForeignKey(Trip, related_name='log_sheets', on_delete=models.CASCADE)
    day_number = models.IntegerField()
    date = models.DateField()
    log_data = models.JSONField()  # stores the structured data to draw the log grid

    class Meta:
        ordering = ['day_number']

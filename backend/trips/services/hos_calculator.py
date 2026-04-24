from datetime import datetime, timedelta

# CONSTANTES
MAX_DRIVING_HOURS = 11
MAX_WINDOW_HOURS = 14
REQUIRED_REST_HOURS = 10
BREAK_AFTER_HOURS = 8
BREAK_DURATION_HOURS = 0.5
WEEKLY_LIMIT_HOURS = 70
FUEL_INTERVAL_MILES = 1000
FUEL_STOP_DURATION = 0.5
PICKUP_DROPOFF_DURATION = 1.0
AVERAGE_SPEED_MPH = 55

def calculate_trip_plan(total_distance_miles, total_duration_hours, current_cycle_used, pickup_location, dropoff_location) -> list:
    stops = []
    current_time = datetime(2024, 1, 1, 6, 0)
    miles_remaining = total_distance_miles
    daily_driving = 0.0
    continuous_driving = 0.0
    cycle_hours = current_cycle_used
    order = 1

    # Agregar stop de pickup
    pickup_stop = {
        'stop_type': 'pickup',
        'location_name': pickup_location,
        'arrival_time': current_time,
        'departure_time': current_time + timedelta(hours=PICKUP_DROPOFF_DURATION),
        'duration_hours': PICKUP_DROPOFF_DURATION,
        'order': order,
        'lat': 0.0,
        'lng': 0.0
    }
    stops.append(pickup_stop)
    current_time = pickup_stop['departure_time']
    cycle_hours += PICKUP_DROPOFF_DURATION
    order += 1

    while miles_remaining > 0:
        if cycle_hours >= WEEKLY_LIMIT_HOURS:
            # Insertar descanso de 34 horas para resetear el ciclo semanal
            rest_stop = {
                'stop_type': 'reset_34hr',
                'location_name': '',
                'arrival_time': current_time,
                'departure_time': current_time + timedelta(hours=34),
                'duration_hours': 34,
                'order': order,
                'lat': 0.0,
                'lng': 0.0
            }
            stops.append(rest_stop)
            current_time = rest_stop['departure_time']
            cycle_hours = 0
            daily_driving = 0
            continuous_driving = 0
            order += 1
            continue

        if daily_driving >= MAX_DRIVING_HOURS:
            # Insertar descanso de 10 horas al final del día
            rest_stop = {
                'stop_type': 'rest_10hr',
                'location_name': '',
                'arrival_time': current_time,
                'departure_time': current_time + timedelta(hours=REQUIRED_REST_HOURS),
                'duration_hours': REQUIRED_REST_HOURS,
                'order': order,
                'lat': 0.0,
                'lng': 0.0
            }
            stops.append(rest_stop)
            current_time = rest_stop['departure_time']
            daily_driving = 0
            continuous_driving = 0
            order += 1
            continue

        if continuous_driving >= BREAK_AFTER_HOURS:
            # Insertar descanso de 30 minutos después de cada 8 horas de conducción
            break_stop = {
                'stop_type': 'rest_30min',
                'location_name': '',
                'arrival_time': current_time,
                'departure_time': current_time + timedelta(hours=BREAK_DURATION_HOURS),
                'duration_hours': BREAK_DURATION_HOURS,
                'order': order,
                'lat': 0.0,
                'lng': 0.0
            }
            stops.append(break_stop)
            current_time = break_stop['departure_time']
            continuous_driving = 0
            order += 1
            continue

        if miles_remaining < total_distance_miles and (total_distance_miles - miles_remaining) % FUEL_INTERVAL_MILES < AVERAGE_SPEED_MPH:
            # Insertar parada de combustible cada 1000 millas
            fuel_stop = {
                'stop_type': 'fuel',
                'location_name': '',
                'arrival_time': current_time,
                'departure_time': current_time + timedelta(hours=FUEL_STOP_DURATION),
                'duration_hours': FUEL_STOP_DURATION,
                'order': order,
                'lat': 0.0,
                'lng': 0.0
            }
            stops.append(fuel_stop)
            current_time = fuel_stop['departure_time']
            cycle_hours += FUEL_STOP_DURATION
            order += 1
            continue

        # Calcular segmento de conducción
        max_before_break = BREAK_AFTER_HOURS - continuous_driving
        max_before_daily_limit = MAX_DRIVING_HOURS - daily_driving
        max_before_fuel = (FUEL_INTERVAL_MILES - ((total_distance_miles - miles_remaining) % FUEL_INTERVAL_MILES)) / AVERAGE_SPEED_MPH
        drive_hours = min(max_before_break, max_before_daily_limit, max_before_fuel, miles_remaining / AVERAGE_SPEED_MPH)
        drive_hours = max(drive_hours, 0.01)  # prevent infinite loop

        # Agregar stop de conducción
        driving_stop = {
            'stop_type': 'driving',
            'location_name': 'En route',
            'arrival_time': current_time,
            'departure_time': current_time + timedelta(hours=drive_hours),
            'duration_hours': drive_hours,
            'order': order,
            'lat': 0.0,
            'lng': 0.0
        }
        stops.append(driving_stop)
        current_time = driving_stop['departure_time']
        miles_remaining -= drive_hours * AVERAGE_SPEED_MPH
        daily_driving += drive_hours
        continuous_driving += drive_hours
        cycle_hours += drive_hours
        order += 1

    # Agregar stop de dropoff
    dropoff_stop = {
        'stop_type': 'dropoff',
        'location_name': dropoff_location,
        'arrival_time': current_time,
        'departure_time': current_time + timedelta(hours=PICKUP_DROPOFF_DURATION),
        'duration_hours': PICKUP_DROPOFF_DURATION,  # must be exactly 1.0, not calculated from datetime difference
        'order': order,
        'lat': 0.0,
        'lng': 0.0
    }
    stops.append(dropoff_stop)

    return stops

import datetime

def generate_log_sheets(stops: list) -> list:
    def create_empty_log_sheet(day_number, date):
        return {
            'day_number': day_number,
            'date': date.strftime('%Y-%m-%d'),
            'log_data': {
                'off_duty': [],
                'sleeper': [],
                'driving': [],
                'on_duty': [],
                'total_off_duty': 0.0,
                'total_sleeper': 0.0,
                'total_driving': 0.0,
                'total_on_duty': 0.0
            }
        }

    def add_to_log(log_data, state, start_hour, end_hour):
        log_data[state].append({'start_hour': start_hour, 'end_hour': end_hour})
        log_data[f'total_{state}'] += (end_hour - start_hour)

    def fill_gaps(log_sheet, current_time):
        while current_time < 24.0:
            add_to_log(log_sheet['log_data'], 'off_duty', current_time, min(current_time + 1, 24.0))
            current_time += 1

    log_sheets = {}
    day_number = 1

    for stop in stops:
        arrival_date = stop['arrival_time'].date()
        departure_date = stop['departure_time'].date()

        if arrival_date not in log_sheets:
            log_sheets[arrival_date] = create_empty_log_sheet(day_number, arrival_date)
            day_number += 1

        current_log_sheet = log_sheets[arrival_date]

        start_hour = stop['arrival_time'].hour + stop['arrival_time'].minute / 60
        end_hour = stop['departure_time'].hour + stop['departure_time'].minute / 60

        if departure_date > arrival_date:
            end_hour = 24.0

        if stop['stop_type'] == 'driving':
            add_to_log(current_log_sheet['log_data'], 'driving', start_hour, end_hour)
        elif stop['stop_type'] == 'rest_10hr':
            add_to_log(current_log_sheet['log_data'], 'sleeper', start_hour, min(start_hour + 8.0, end_hour))
            if end_hour > start_hour + 8.0:
                add_to_log(current_log_sheet['log_data'], 'off_duty', start_hour + 8.0, end_hour)
        elif stop['stop_type'] in ['rest_30min', 'pickup', 'dropoff', 'fuel']:
            add_to_log(current_log_sheet['log_data'], 'on_duty', start_hour, end_hour)
        else:
            add_to_log(current_log_sheet['log_data'], 'off_duty', start_hour, end_hour)

    for log_sheet in log_sheets.values():
        fill_gaps(log_sheet, 24.0)

    sorted_log_sheets = sorted(log_sheets.values(), key=lambda x: x['day_number'])
    return sorted_log_sheets

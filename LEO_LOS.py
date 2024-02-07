# Satellite altitudes in kilometers
satellite_altitude_min_km = 590
satellite_altitude_max_km = 630

# Calculate the horizon distance for both altitudes
horizon_distance_min_km = 3.57 * math.sqrt(satellite_altitude_min_km)
horizon_distance_max_km = 3.57 * math.sqrt(satellite_altitude_max_km)

# Estimate the LOS duration in minutes for both altitudes
los_duration_min_minutes = (2 * horizon_distance_min_km) / satellite_speed_kmps / 60
los_duration_max_minutes = (2 * horizon_distance_max_km) / satellite_speed_kmps / 60

# Averaging the LOS durations
average_los_duration_minutes = (los_duration_min_minutes + los_duration_max_minutes) / 2

horizon_distance_min_km, horizon_distance_max_km, los_duration_min_minutes, los_duration_max_minutes, average_los_duration_minutes
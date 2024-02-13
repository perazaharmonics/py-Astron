import math
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


def get_julian_day(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return JD

def calculate_sun_longitude(utc_hour):
    # Calculate the fraction of the day
    fraction_of_day = utc_hour / 24.0
    # Calculate the sun's longitude, adjusting for it being at 0 degrees at 12:00 UTC
    sun_longitude = (fraction_of_day * 360) - 180
    return sun_longitude

def get_sun_position(year, month, day):
    epsilon = 23.4393 - 0.0000004 * year
    JD = get_julian_day(year, month, day)
    n = JD - 2451545.0
    L = (280.460 + 0.9856474 * n) % 360
    g = (357.528 + 0.9856003 * n) % 360
    lambda_sun = L + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
    alpha = math.atan2(math.cos(math.radians(epsilon)) * math.sin(math.radians(lambda_sun)), math.cos(math.radians(lambda_sun)))
    alpha = math.degrees(alpha)
    delta = math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(lambda_sun)))
    delta = math.degrees(delta)
    return alpha % 360, delta

def calculate_azimuth_elevation(observer_lat, observer_lon, year, month, day, utc_hour):
    # Constants
    observer_lat_rad = math.radians(observer_lat)
    
    # Get Julian Day
    JD = get_julian_day(year, month, day)
    # Calculate the sun's position
    _, dec_degrees = get_sun_position(year, month, day)
    dec_rad = math.radians(dec_degrees)
    
    # Calculate Local Sidereal Time (LST)
    T = (JD - 2451545.0) / 36525.0
    LST_hours = (6.697374558 + 24.06570982441908 * (JD - 2451545) + T*T*0.000026 * (T)) % 24
    LST = LST_hours * 15.0  # Convert hours to degrees
    
    # Calculate Hour Angle (HA)
    HA = LST + observer_lon - ra
    HA_rad = math.radians(HA)
    
    # Elevation
    elevation_rad = math.asin(math.sin(observer_lat_rad)*math.sin(dec_rad) + math.cos(observer_lat_rad)*math.cos(dec_rad)*math.cos(HA_rad))
    elevation = math.degrees(elevation_rad)
    
    # Azimuth
    azimuth_rad = math.atan2(-math.sin(HA_rad), (math.tan(dec_rad)*math.cos(observer_lat_rad) - math.sin(observer_lat_rad)*math.cos(HA_rad)))
    azimuth = math.degrees(azimuth_rad) + 180.0  # Adjusting azimuth to be measured from the North
    
    return azimuth, elevation

# User input section
year = int(input("Enter the year: "))
month = int(input("Enter the month: "))
day = int(input("Enter the day: "))
observer_lat = float(input("Enter the observer's latitude (negative for South): "))
observer_lon = float(input("Enter the observer's longitude (negative for West): "))

# Get the current UTC time
current_utc_time = datetime.utcnow()
# For demonstration, using the current UTC hour; for precise calculations, consider minutes and seconds
utc_hour = current_utc_time.hour + current_utc_time.minute / 60 + current_utc_time.second / 3600
sun_longitude = calculate_sun_longitude(utc_hour)
ra, dec = get_sun_position(year, month, day)
print(f"Right Ascension: {ra:.2f} degrees, Declination: {dec:.2f} degrees")

# Calculate sun's azimuth and elevation
azimuth, elevation = calculate_azimuth_elevation(observer_lat, observer_lon, year, month, day, utc_hour)
print(f"The sun's azimuth is {azimuth:.2f} degrees and elevation is {elevation:.2f} degrees")

# Plotting with Cartopy
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
ax.set_global()
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

# Plot the sun's position
ax.plot(sun_longitude, dec, 'o', color='yellow', markersize=12, transform=ccrs.Geodetic(), label='Sun Position')

plt.legend()
plt.show()

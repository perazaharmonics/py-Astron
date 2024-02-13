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

# User input section
year = int(input("Enter the year: "))
month = int(input("Enter the month: "))
day = int(input("Enter the day: "))

# Get the current UTC time
current_utc_time = datetime.utcnow()
# For demonstration, using the current UTC hour; for precise calculations, consider minutes and seconds
utc_hour = current_utc_time.hour + current_utc_time.minute / 60 + current_utc_time.second / 3600
sun_longitude = calculate_sun_longitude(utc_hour)
ra, dec = get_sun_position(year, month, day)
print(f"Right Ascension: {ra:.2f} degrees, Declination: {dec:.2f} degrees")

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

import math
import csv
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import cartopy.crs as ccrs
import cartopy.feature as cfeature

file_path = 'sun_positions.csv'  # Adjusted for simplicity, ensure the path is correct for your environment

def get_sub_solar_point(date):
    """
    Calculate the latitude (declination) and longitude of the sub-solar point for a given datetime in UTC.
    """
    J2000 = datetime(2000, 1, 1, 12)  # Reference epoch for J2000
    days_since_J2000 = (date - J2000).total_seconds() / 86400.0
    
    # Simplified formula for declination
    axial_tilt = 23.44
    orbital_position = (days_since_J2000 / 365.25) * 360 % 360
    declination = axial_tilt * math.sin(math.radians(orbital_position))
    
    # Simplified formula for longitude
    utc_hour = date.hour + date.minute / 60 + date.second / 3600
    longitude = ((utc_hour - 12) * 15) % 360
    if longitude > 180:
        longitude -= 360
    
    return declination, longitude

def generate_monthly_data(year, month, utc_offset):
    """
    Generate data for the sub-solar point's position for every hour of a given month and save it to a CSV file.
    """
    days_in_month = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['DateTime', 'Latitude', 'Longitude'])
        
        for day in range(1, days_in_month + 1):
            for hour in range(24):
                current_time = datetime(year, month, day, hour) - timedelta(hours=utc_offset)
                latitude, longitude = get_sub_solar_point(current_time)
                writer.writerow([current_time.isoformat(), latitude, longitude])

def read_sun_positions_csv():
    """
    Read the generated CSV file and return the positions as lists of latitudes and longitudes.
    """
    latitudes, longitudes = [], []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            latitudes.append(float(row['Latitude']))
            longitudes.append(float(row['Longitude']))
    return latitudes, longitudes

def animate(i):
    """
    Update the position of the sun marker for frame i in the animation.
    """
    sun_marker.set_data([longitudes[i]], [latitudes[i]])
    return sun_marker,

# Main execution
year = int(input("Enter the year: "))
month = int(input("Enter the month: "))
day = int(input("Enter the day: "))
utc_offset = float(input("Enter the local time offset from UTC (e.g., -4 to -5 for EST): "))

generate_monthly_data(year, month, utc_offset)
latitudes, longitudes = read_sun_positions_csv()

# Setup for animation
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

sun_marker, = ax.plot(longitudes[0], latitudes[0], 'o', color='yellow', markersize=12, transform=ccrs.Geodetic(), label='Sub-Solar Point')

ani = FuncAnimation(fig, animate, frames=len(longitudes), blit=True, interval=200)

plt.legend()
plt.show()

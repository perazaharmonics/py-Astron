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

def calculate_sun_longitude(local_hour, utc_offset):
    # Calculate the fraction of the day
    utc_hour = local_hour - utc_offset
    fraction_of_day = utc_hour / 24.0
    # Calculate the sun's longitude, adjusting for it being at 0 degrees at 12:00 UTC
    sun_longitude = (fraction_of_day * 360) - 180
    return sun_longitude
   
def get_declination(year, month, day):
    epsilon=23.4393-0.0000004*year # Obliquity of the Earth's axis
    JD=get_julian_day(year, month, day) # Get the Julian Day
    n=JD-2451545.0 # Number of days since January 1, 2000
    L=(280.460+0.9856474*n)%360 # Mean longitude of the Sun
    g=(357.528+0.9856003*n)%360 # Mean anomaly of the Sun
    lambda_sun=L+1.915*math.sin(math.radians(g))+0.020*math.sin(math.radians(2*g)) # Ecliptic longitude of the Sun
    delta=math.asin(math.sin(math.radians(epsilon))*math.sin(math.radians(lambda_sun))) # Declination
    delta=math.degrees(delta) # Convert to degrees
    return delta # Return the declination in degrees

def get_right_ascension(year, month, day):
    epsilon=23.4393-0.0000004*year # Obliquity of the Earth's axis
    JD=get_julian_day(year, month, day) # Get the Julian Day
    n=JD-2451545.0 # Number of days since January 1, 2000
    L=(280.460+0.9856474*n)%360 # Mean longitude of the Sun
    g=(357.528+0.9856003*n)%360 # Mean anomaly of the Sun
    lambda_sun=L+1.915*math.sin(math.radians(g))+0.020*math.sin(math.radians(2*g)) # Ecliptic longitude of the Sun
    alpha=math.atan2(math.cos(math.radians(epsilon))*math.sin(math.radians(lambda_sun)),math.cos(math.radians(lambda_sun))) # Right Ascension
    alpha=math.degrees(alpha) # Convert to degrees
    return alpha # Return the right ascension in degrees

def calculate_azimuth(observer_lat, observer_lon, year, month, day, local_hour, utc_offset):
    # Constants
    observer_lat_rad=math.radians(observer_lat)

    # Adjust local hour to UTC hour
    utc_hour=local_hour+utc_offset
    
    # Get Julian Day
    JD=get_julian_day(year, month, day)

    # Calculate the sun's position
    ra=get_right_ascension(year, month, day)
    dec=get_declination(year, month, day)
    ra_rad=math.radians(ra)
    dec_rad=math.radians(dec)

    # Calculate Local Sidereal Time (LST)
    T=(JD-2451545.0)/36525.0                # Julian Centuries since J2000
    sdshours=24.06570982441908*(JD-2451545) # Sidereal Time in hours since J2000
    GSTJ2000=6.697374558                  # Greenwich Sidereal Time at J2000
    corr=T*T*0.000026*(T)                # Correction for nutation, precession, and aberration

    LST_hours=(GSTJ2000+sdshours+corr)%24
    LST=LST_hours*15.0 # Convert hours to degrees

    # Calculate Hour Angle (HA)
    HA=LST-observer_lon-ra
    HA_rad=math.radians(HA)

    # Azimuth
    azimuth_rad=math.atan2(math.sin(HA_rad),math.cos(HA_rad)*math.sin(observer_lat_rad)-math.tan(math.radians(dec))*math.cos(observer_lat_rad))
    

    azimuth=math.degrees(azimuth_rad)
    return azimuth

def calculate_elevation(observer_lat, observer_lon, year, month, day, local_hour, utc_offset):
    # Constants
    observer_lat_rad = math.radians(observer_lat)
    
    # Adjust local hour to UTC hour
    utc_hour = local_hour - utc_offset
    
    # Get Julian Day
    JD = get_julian_day(year, month, day)
    
    # Calculate the sun's position
    ra=get_right_ascension(year, month, day)
    dec=get_declination(year, month, day)
    ra_rad = math.radians(ra)
    dec_rad = math.radians(dec)

    # Calculate Local Sidereal Time (LST)
    T=(JD-2451545.0)/36525.0                # Julian Centuries since J2000
    sdshours=24.06570982441908*(JD-2451545) # Sidereal Time in hours since J2000
    GSTJ2000=6.697374558                    # Greenwich Sidereal Time at J2000
    corr=T*T*0.000026*(T)                # Correction for nutation, precession, and aberration    
    # Calculate Local Sidereal Time (LST)
    T = (JD - 2451545.0) / 36525.0
    LST_hours=(GSTJ2000+sdshours+corr)%24
    LST = LST_hours * 15.0  # Convert hours to degrees 360/24 (degrees per hours) = 15 degrees per hour
    
    # Calculate Hour Angle (HA)
    HA = LST + observer_lon - ra
    HA_rad = math.radians(HA)
    
    # Elevation
    elevation_rad = math.asin(math.sin(observer_lat_rad)*math.sin(dec_rad) + math.cos(observer_lat_rad)*math.cos(dec_rad)*math.cos(HA_rad))
    elevation = math.degrees(elevation_rad)
    
    return elevation

# User input section
year = int(input("Enter the year: "))
month = int(input("Enter the month: "))
day = int(input("Enter the day: "))
observer_lat = float(input("Enter the observer's latitude (negative for South): "))
observer_lon = float(input("Enter the observer's longitude (negative for West): "))
utc_offset = float(input("Enter the local time offset from UTC (e.g., -4 to -5 for EST): "))

# Get the current UTC time
current_utc_time = datetime.utcnow()
current_local_time = current_utc_time + timedelta(hours=utc_offset)

# For demonstration, using the current UTC hour; for precise calculations, consider minutes and seconds
local_hour = current_local_time.hour + current_local_time.minute / 60 + current_local_time.second / 3600
sun_longitude = calculate_sun_longitude(local_hour, utc_offset)
ra, dec = get_sun_position(year, month, day)
print(f"Right Ascension: {ra:.2f} degrees, Declination: {dec:.2f} degrees")

# Calculate sun's azimuth and elevation
azimuth, elevation = calculate_azimuth_elevation(observer_lat, observer_lon, year, month, day, local_hour, utc_offset)
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

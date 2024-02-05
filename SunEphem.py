import math

def get_julian_day(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5
    return JD

def get_sun_position(year, month, day):
    # Constants
    epsilon = 23.4393 - 0.0000004 * year  # Obliquity of the ecliptic
    JD = get_julian_day(year, month, day)
    n = JD - 2451545.0
    L = (280.460 + 0.9856474 * n) % 360
    g = (357.528 + 0.9856003 * n) % 360

    # Mean longitude of the Sun, corrected for the aberration of light
    lambda_sun = L + 1.915 * math.sin(math.radians(g)) + 0.020 * math.sin(math.radians(2 * g))
    # Right Ascension
    alpha = math.atan2(math.cos(math.radians(epsilon)) * math.sin(math.radians(lambda_sun)), math.cos(math.radians(lambda_sun)))
    alpha = math.degrees(alpha)
    # Declination
    delta = math.asin(math.sin(math.radians(epsilon)) * math.sin(math.radians(lambda_sun)))
    delta = math.degrees(delta)

    return alpha % 360, delta

# Example: Calculate sun's position on 2024-02-05
year = 2024
month = 2
day = 5
ra, dec = get_sun_position(year, month, day)
print(f"Right Ascension: {ra:.2f} degrees, Declination: {dec:.2f} degrees")
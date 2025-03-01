import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import itertools
import string
import random

# Raster x: 1->50 y:A-Y
import string

letters = string.ascii_uppercase[:25]  # 'A' to 'Y'
numbers = range(1, 51)  # 1 to 50

# Generate locations as strings like "A1", "A2", ..., "Y50"
locations = [f"{letter}{num}" for letter in letters for num in numbers]

# Köppen-Geiger classifications
koppen_geiger = ["Af", "Am", "Aw", "Cfb", "Cfa", "Csb", "Csc", "Dfb", "Dfc", "ET"]

# Assign a random classification to each location
location_koppen = {location: random.choice(koppen_geiger) for location in locations}
grond_loc = {}
for location in location_koppen:
    # Terrein
    terreinen = ["Bergen", "Heuvels", "Vlaktes", "Woestijnen", "Toendra","Moerassen","Savanne","Tropisch regenwoud","Steppes"]
    terrein = random.choice(terreinen)

    # Ondergrond
    ondergronden = ["Zand","Klei","Leem","Silt","Kalksteen","Graniet","Basalt","Veen"]
    ondergrond = random.choice(ondergronden)
    grond_loc[location] = [terrein, ondergrond]
# print(location_koppen)

# Generate daily timestamps from start to end date
start_date = datetime.utcfromtimestamp(1672527600)  # 2023-01-01
end_date = datetime.utcfromtimestamp(1704063599)    # 2024-12-31
date_range = [start_date + timedelta(days=i) for i in range(0, (end_date - start_date).days + 1, 70)]

# Function to generate weather data with dependencies and extremes
def generate_weather(koppen, day_of_year):
    # Normalize day of the year for a sine wave (0 to 1)
    seasonal_factor = np.sin(2 * np.pi * day_of_year / 365)
    
    if koppen in ["Af", "Am", "Aw"]:  # Tropical
        temp_base = 28  # Average tropical temperature
        temp_variation = 5 * seasonal_factor  # More extremes
        temp = temp_base + temp_variation + np.random.uniform(-5, 5)  # Random fluctuation
        
        cloud_cover = np.random.uniform(50, 100)  # Higher average cloud cover
        precipitation = np.random.uniform(0, cloud_cover / 10)  # Correlated to cloud cover
        humidity = 70 + (cloud_cover / 3)  # Correlation: more clouds => higher humidity
    elif koppen in ["Cfb", "Cfa", "Csb", "Csc"]:  # Temperate
        temp_base = 10
        temp_variation = 15 * seasonal_factor  # More extreme seasonal change
        temp = temp_base + temp_variation + np.random.uniform(-10, 10)
        
        cloud_cover = np.random.uniform(20, 80)
        precipitation = np.random.uniform(0, cloud_cover / 8)
        humidity = 60 + (cloud_cover / 4)
    elif koppen in ["Dfb", "Dfc", "ET"]:  # Cold
        temp_base = -10
        temp_variation = 20 * seasonal_factor
        temp = temp_base + temp_variation + np.random.uniform(-15, 10)
        
        cloud_cover = np.random.uniform(10, 70)
        precipitation = np.random.uniform(0, cloud_cover / 12)
        humidity = 40 + (cloud_cover / 5)
    
    # Other variables with minor or no dependency
    pressure = np.random.uniform(1000, 1030) - (temp / 20)  # Colder temps => higher pressure
    wind_speed = np.random.uniform(5, 25)
    wind_dir = np.random.uniform(0, 360)

    # Seismische activiteit
    # Genereer een log-normale magnitude en clip naar [1, 10]
    magnitude = np.random.lognormal(0, 1.5, 10000)[0]
    magnitude = int(np.clip(magnitude, 1, 10))

    # Maak mmi afhankelijk van magnitude + toegevoegde ruis
    mmi_base = magnitude + np.random.normal(0, 1.5)  # Kleine variatie
    mmi = int(np.clip(mmi_base, 1, 12))  # Clip binnen [1, 12]

    seismische_activiteit = (magnitude, mmi)

    # UV-index
    uv_index = np.random.lognormal(0.5, 1.5, 10000)[0]
    uv_index = int(np.clip(uv_index, 1, 13))

    # Vulkanische activiteit
    uitbarsting_gemeten = random.choices([0, 1], weights=(80, 20))[0]
    giftigheid_vrijgekomen_stoffen = (uitbarsting_gemeten * (25-wind_speed))/25



    return temp, pressure, wind_speed, wind_dir, humidity, cloud_cover, precipitation, seismische_activiteit, uv_index, uitbarsting_gemeten, giftigheid_vrijgekomen_stoffen

# Generate the dataset
data = []

for location in locations:
    koppen = location_koppen[location]
    for date in date_range:
        day_of_year = date.timetuple().tm_yday
        temp, pressure, wind_speed, wind_dir, humidity, cloud_cover, precipitation, seismische_activiteit, uv_index, uitbarsting_gemeten, giftigheid_vrijgekomen_stoffen = generate_weather(koppen, day_of_year)
        data.append([int(date.timestamp()), location, koppen, temp, pressure, wind_speed, wind_dir, humidity, cloud_cover, precipitation, seismische_activiteit, uv_index, grond_loc[location][0], grond_loc[location][1], uitbarsting_gemeten, giftigheid_vrijgekomen_stoffen])

# Create a DataFrame
columns = [
    "UNIXTimestamp", "Location", "LocationKoppenGeigerClassification",
    "AirTemperatureCelsius", "AirPressure_hPa", "WindSpeed_kmh",
    "WindDirection_deg", "Humidity_percent", "CloudCoverage_percent", "Precipitation_mm", "Seismische Activiteit", "UV index", "Terrein", "Ondergrond", "Uitbarsting gemeten", "Giftigheid vrijgekomen stoffen"
]
df = pd.DataFrame(data, columns=columns)

# Save to CSV
df.to_csv("./Eigen data/dataset.csv", index=False)

# Confirm success
print(f"Dataset with {len(df)} rows saved to './Eigen data/dataset.csv'.")

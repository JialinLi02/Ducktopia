import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
weather_file = r"C:\Documents\VS Code\Hacktopia\Eigen data\dataset.csv"
weather_data = pd.read_csv(weather_file)

# Group by Location and calculate the sum of precipitation, then multiply by 7 for annual precipitation
grouped_data = weather_data.groupby("Location").agg({
    "AirTemperatureCelsius": "mean",
    "AirPressure_hPa": "mean",
    "WindSpeed_kmh": "mean",
    "CloudCoverage_percent": "mean",
    "Precipitation_mm": "sum",  # Sum of daily precipitation
    "UV index": lambda x: x.quantile(0.75),  # Use the 75th percentile for UV index
    "LocationKoppenGeigerClassification": lambda x: x.mode()[0]  # Use the most common climate type
}).reset_index()

# Calculate annual precipitation (sum of daily precipitation * 7)
grouped_data["AnnualPrecipitation"] = grouped_data["Precipitation_mm"] * 7

# Rename columns for clarity
grouped_data.rename(columns={
    "AirTemperatureCelsius": "AverageTemperature",
    "AirPressure_hPa": "AveragePressure",
    "WindSpeed_kmh": "AverageWindSpeed",
    "CloudCoverage_percent": "AverageCloudCoverage",
    "Precipitation_mm": "TotalPrecipitation",  # Rename to reflect total precipitation
    "UV index": "UVIndex75thPercentile",  # Rename to reflect 75th percentile
    "LocationKoppenGeigerClassification": "MostCommonClimateType"
}, inplace=True)

# Display the grouped data
print(grouped_data.head())

# Define scoring functions
def score_temperature(temp):
    if 10 <= temp <= 30:
        return 100
    # Smooth curve for temperature outside the ideal range
    else:
        penalty = max(0, 100 - (temp - 20)**2 * 0.5)  # Quadratic penalty
        return penalty

def score_pressure(pressure):
    if 950 <= pressure <= 1050:
        return 100
    # Smooth penalty around 1000 using a sigmoid-like function
    return max(0, 100 - 100 / (1 + abs(pressure - 1000) * 0.1))

def score_wind_speed(wind_speed):
    if wind_speed <= 10:
        return 100  # No effect for light winds
    elif wind_speed <= 20:
        return 80  # Mild penalty for moderate winds
    else:
        return max(0, 100 - (wind_speed - 20) * 2)

def score_cloud_coverage(cloud_cover):
    if 30 <= cloud_cover <= 70:
        return 100
    elif cloud_cover < 30:
        return 90  # Light penalty for clear skies
    elif cloud_cover > 70:
        return 90  # Light penalty for overcast skies
    return max(0, 100 - abs(cloud_cover - 50) * 2)

def score_precipitation(annual_precipitation):
    """
    Assign a score based on annual precipitation.
    The best range is around 500-1200 mm per year.
    """
    if 500 <= annual_precipitation <= 1200:
        return 100  # Ideal balance of rain
    elif 250 <= annual_precipitation < 500 or 1200 < annual_precipitation <= 1500:
        return 80  # Slightly dry or wet, but still good
    elif 1500 < annual_precipitation <= 1800 or 150 < annual_precipitation < 250:
        return 60  # Noticeably dry or wet
    elif 1800 < annual_precipitation <= 2500 or 50 < annual_precipitation < 150:
        return 40  # Very wet or quite dry
    else:  # Extreme dry or wet conditions
        return 20  # Not ideal for livability


def score_uv_index(uv_index):
    """
    Assign a score based on the UV index (75th percentile).
    Lower UV index is better.
    """
    if uv_index <= 5:
        return 100  # Best score
    elif uv_index <= 7:
        return 75
    elif uv_index <= 10:
        return 50
    else:  # UV index > 10
        return 25  # Worst score

def score_climate_type(climate_type):
    climate_scores = {
        "Cfa": 100,
        "Cfb": 98,
        "Csb": 95,
        "Csc": 92,
        "Af": 85,
        "Am": 80,
        "Aw": 75,
        "Dfb": 65,
        "Dfc": 60,
        "ET": 50
    }
    return climate_scores.get(climate_type, 50)  # Default score of 50 for unknown climate types

# Apply scoring functions to the grouped data
grouped_data["TemperatureScore"] = grouped_data["AverageTemperature"].apply(score_temperature)
grouped_data["PressureScore"] = grouped_data["AveragePressure"].apply(score_pressure)
grouped_data["WindSpeedScore"] = grouped_data["AverageWindSpeed"].apply(score_wind_speed)
grouped_data["CloudCoverageScore"] = grouped_data["AverageCloudCoverage"].apply(score_cloud_coverage)
grouped_data["PrecipitationScore"] = grouped_data["AnnualPrecipitation"].apply(score_precipitation)  # Updated to use annual precipitation
grouped_data["UVScore"] = grouped_data["UVIndex75thPercentile"].apply(score_uv_index)
grouped_data["ClimateScore"] = grouped_data["MostCommonClimateType"].apply(score_climate_type)

# Define weights for each parameter
weights = {
    "TemperatureScore": 0.25,
    "PressureScore": 0.10,
    "WindSpeedScore": 0.10,
    "CloudCoverageScore": 0.10,
    "PrecipitationScore": 0.15,
    "UVScore": 0.10,
    "ClimateScore": 0.20,
}

# Calculate the weather score
grouped_data["WeatherScore"] = (
    grouped_data["TemperatureScore"] * weights["TemperatureScore"] +
    grouped_data["PressureScore"] * weights["PressureScore"] +
    grouped_data["WindSpeedScore"] * weights["WindSpeedScore"] +
    grouped_data["CloudCoverageScore"] * weights["CloudCoverageScore"] +
    grouped_data["PrecipitationScore"] * weights["PrecipitationScore"] +
    grouped_data["UVScore"] * weights["UVScore"] +
    grouped_data["ClimateScore"] * weights["ClimateScore"]
)

# # Sort the data by WeatherScore for better visualization
# grouped_data = grouped_data.sort_values("WeatherScore", ascending=False)

# # Plot the weather scores
# plt.figure(figsize=(12, 8))
# sns.barplot(x="WeatherScore", y="Location", data=grouped_data, palette="viridis")
# plt.title("Weather Scores by Location")
# plt.xlabel("Weather Score (%)")
# plt.ylabel("Location")
# plt.show()

grouped_data["WeatherScore"] = grouped_data["WeatherScore"] // 10

# Display the final results
print(grouped_data[["Location", "WeatherScore"]])

# Write the final results to a CSV file
output_file = r"C:\Documents\VS Code\Hacktopia\Eigen data\weather1_scores.csv"
grouped_data[["Location", "WeatherScore"]].to_csv(output_file, index=False)

print(f"Weather scores have been saved to {output_file}")
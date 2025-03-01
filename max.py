import pandas as pd
import numpy as np
from collections import Counter


data = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset.csv")
plantdata = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Data/dataset_edible_plants.csv")
print(data)


def aggregate_location_data(df):
    
    # Separate numerical, categorical, and tuple columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(exclude=['number']).columns
    tuple_cols = [col for col in df.columns if isinstance(df[col].iloc[0], tuple)]

    # Group by 'Location'
    grouped = df.groupby('Location')

    # Aggregate numerical columns
    aggregated_df = grouped[numerical_cols].mean().reset_index()

    # Aggregate categorical columns
    for col in categorical_cols:
        if col not in tuple_cols:  # Skip tuple columns
            aggregated_df[col] = grouped[col].first().reset_index(drop=True)

    # Aggregate tuple columns
    for col in tuple_cols:
        # Calculate the mean of each element in the tuple
        aggregated_df[col] = grouped[col].apply(lambda x: tuple(np.mean(list(x), axis=0)))

    return aggregated_df

data_agg = aggregate_location_data(data)


## Water availability
def cal_water_availability(rain, temp):
    return 0.7 * rain - 0.2 *temp

def cal_water_th(data):
    th_moderate = np.percentile(data, 33)
    th_high = np.percentile(data, 66)
    return th_moderate, th_high

def water_availability_cat(water_availability, th_moderate, th_high):
    new_list = []
    for i in water_availability: 
        if i > th_high: 
            new_list.append("high")
        elif i > th_moderate:
            new_list.append("moderate")
        else: new_list.append("low")
    return new_list


##Nutscore planten
## Klimaten voor planten: Temperate, Mediterranean, Arid, Tropical, Polar
## koppen_geiger = ["Af", "Am", "Aw", "Cfb", "Cfa", "Csb", "Csc", "Dfb", "Dfc", "ET"]

# Define the mapping dictionary
koppen_to_climate = {
    "Af": "Tropical",
    "Am": "Tropical",
    "Aw": "Tropical",
    "Cfb": "Temperate",
    "Cfa": "Temperate",
    "Csb": "Mediterranean",
    "Csc": "Mediterranean",
    "Dfb": "Temperate",
    "Dfc": "Temperate",
    "ET": "Polar"
}

def map_koppen_to_climate(koppen_values):
    """Maps a list of Köppen-Geiger values to their climate type."""
    return [koppen_to_climate.get(value, "Unknown") for value in koppen_values]

def plantsoorten(climate, WA):
    

def calculate_plantscores(plant_data, weather_data):
    water_availability_set = []
    rainfall_set = weather_data["Precipitation_mm"]
    temp_set = weather_data["AirTemperatureCelsius"]
    for i in range(0,len(rainfall_set)):
        a = cal_water_availability(rainfall_set[i], temp_set[i])
        water_availability_set.append(a)
    
    moderate, high = cal_water_th(water_availability_set)

    WA_categories = water_availability_cat(water_availability_set, moderate, high)
    WA_categories = list(WA_categories)
    weather_data['WA'] = WA_categories

    
    return weather_data



dummydata = []
test = calculate_plantscores(plantdata,data_agg )
value_counts = Counter(test["WA"])
print(value_counts)



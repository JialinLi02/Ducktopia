import pandas as pd
import numpy as np
from collections import Counter


data_agg = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset_aggregated.csv")
plantdata = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Data/dataset_edible_plants.csv")






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
            new_list.append("High")
        elif i > th_moderate:
            new_list.append("Moderate")
        else: new_list.append("Low")
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

def food_score(x,y,z):
    return x * (y +  z)

def plantscores(climate, WA, plant_data):
    plant_climates = plant_data["Growth Climate"]
    plant_water = plant_data["Watering Needs"]
    plant_scores = []
    climate = map_koppen_to_climate(climate)

    for i in range(0,len(climate)):
        size = 0
        prot = 0
        kcal = 0
        counter = 0
        clim = climate[i]
        water = WA[i]
        for j in range(0,len(plant_climates)):
            if plant_climates[j] == clim:
                if plant_water[j] == water:
                    size += plant_data["Weight when Full Grown (kg)"][j]
                    prot += plant_data["Proteins per 100g (g)"][j]
                    kcal += plant_data["Kcal per 100g"][j]
                    counter += 1
        if counter > 0: plant_scores.append(food_score(size/counter, prot/counter, kcal/counter))
        else: plant_scores.append(0)
    plant_scores = (plant_scores/max(plant_scores)) * 10
    return plant_scores
            

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

    plant_scores = plantscores(weather_data["LocationKoppenGeigerClassification"], weather_data['WA'], plant_data) 
    print("Unique plant scores:", set(plant_scores))
    return plant_scores


Foodscore = calculate_plantscores(plantdata,data_agg )
Location = data_agg["Location"]

print(Foodscore)


combined_df = pd.DataFrame({
    'Location': Location,
    'Foodscore': Foodscore
})

combined_df.to_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/food_scores.csv", index=False)


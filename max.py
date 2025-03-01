## Water availability
def cal_water_availability(rain, temp):
    return 0.7*rain - 0.2 *temp

def



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




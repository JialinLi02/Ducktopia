import pandas as pd
import ast
import numpy as np

csv_file = "/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset_aggregated.csv"
data2 = pd.read_csv(csv_file)





data = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset.csv")
food_scores = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Final_scores/food_scores.csv")

# Aggregate the dataset
data["Seismische Activiteit"] = data["Seismische Activiteit"].apply(ast.literal_eval)

# Step 2: Split tuple into separate columns
data[["Seismische_1", "Seismische_2"]] = pd.DataFrame(data["Seismische Activiteit"].tolist(), index=data.index)

# Step 3: Perform groupby and compute mean for each tuple component separately
grouped_data = data.groupby("Location").agg({
    "Seismische_1": "mean",
    "Seismische_2": "mean",
    "Giftigheid vrijgekomen stoffen": "mean",
    "Precipitation_mm": "mean",
    "Uitbarsting gemeten": "sum",
}).reset_index()

# Step 4: Combine back into a tuple
grouped_data["Seismische Activiteit"] = grouped_data.apply(lambda row: (row["Seismische_1"], row["Seismische_2"]), axis=1)

# Step 5: Drop intermediate columns
grouped_data = grouped_data.drop(columns=["Seismische_1", "Seismische_2"])


grouped_data['Food score'] = food_scores['Foodscore']


# Function to determine duck encounter probability
def bepaal_kans_op_eenden(food_value, giftige_lucht, seismic_score, regen):
    if food_value > 8:
        food_score = 3
    elif food_value > 7:
        food_score = 2
    else:
        food_score = 1

    if 0.25 < giftige_lucht < 0.35:  # Fixed bitwise & issue
        lucht_score = 3
    elif 0.15 < giftige_lucht < 0.45:
        lucht_score = 2
    else:
        lucht_score = 1
    
    if seismic_score[0]>7 or seismic_score[1]>7:
        ssm_score = 3
    elif seismic_score[0]>4 or seismic_score[1]>4:
        ssm_score = 2
    else:
        ssm_score = 1
        
    if regen > 4:
        regen_score = 3
    elif regen > 3:
        regen_score = 2
    else:
        regen_score = 1
        
    total_score = (5*food_score + 3*lucht_score + 2*ssm_score + 4*regen_score)*10/42
    return 10 - round(total_score)

# Function to determine seismic score
def bepaal_seismische_score(seismische_score, giftige_gassen, aantal_aardbevingen):
    if seismische_score[0]>8 or seismische_score[1]>8:
        ssm_score = 4
    elif seismische_score[0]>6 or seismische_score[1]>6:
        ssm_score = 3
    elif seismische_score[0]>4 or seismische_score[1]>4:
        ssm_score = 2
    else:
        ssm_score = 1
    
    if giftige_gassen > 0.5:
        gas_score = 4
    elif giftige_gassen > 0.4:
        gas_score = 3
    elif giftige_gassen > 0.3:
        gas_score = 2
    else:
        gas_score = 1

    if aantal_aardbevingen > 0.3:  # Fixed variable typo
        beving_score = 4
    elif aantal_aardbevingen > 0.2:
        beving_score = 3
    elif aantal_aardbevingen > 0.1:
        beving_score = 2
    else:
        beving_score = 1

    total_score = (beving_score + gas_score + ssm_score)*10/12
    return 10 - round(total_score)

# Now applying the functions after they are defined
grouped_data['Duck score'] = grouped_data.apply(lambda row: bepaal_kans_op_eenden(row['Food score'], row['Giftigheid vrijgekomen stoffen'], row['Seismische Activiteit'], row['Precipitation_mm']), axis=1)


grouped_data['Seismic score'] = grouped_data.apply(lambda row: bepaal_seismische_score(row['Seismische Activiteit'], row['Giftigheid vrijgekomen stoffen'], row['Uitbarsting gemeten']), axis=1)

locations = data2["Location"]
wind = data2["WindSpeed_kmh"]
uitbarstingen  = [1 if score > 0.25 else 0 for score in data2["Uitbarsting gemeten"]]
seis = grouped_data['Seismic score']

combined_df = pd.DataFrame({
    'Location': locations,
    'Windspeed': wind
})

combined_df.to_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Final_scores/wind_scores.csv", index=False)

combined_df = pd.DataFrame({
    'Location': locations,
    'uitbarstingen': uitbarstingen
})

combined_df.to_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Final_scores/uitbarsting_scores.csv", index=False)

combined_df = pd.DataFrame({
    'Location': locations,
    'seismic': seis
})

combined_df.to_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Final_scores/seismic_scores.csv", index=False)


# Determining odds of encountering dangerous ducks

import pandas as pd

data = pd.read_csv("C:/Users/herli/Downloads/AE/Ducktopia/Eigen data/dataset_aggregated.csv")
data.head()


import pandas as pd
import numpy as np

"""
Input:      food_value, giftige_lucht, seismic_score, regen
Output:     kans op eenden op schaal van 1 (lage kans) tot 3 (hoge kans)
"""
def bepaal_kans_op_eenden(food_value, giftige_lucht, seismic_score, regen):
    for location in data.location:
        if food_value > 8:
            food_score = 3
        elif food_value > 7:
            food_score = 2
        else:
            food_score = 1

        if giftige_lucht > 0.25 AND giftige_lucht < 0.35:
            lucht_score = 3
        elif giftige_lucht > 0.15 AND giftige_lucht < 0.45:
            lucht_score = 2
        else:
            lucht_score = 1

        if seismic_score > 7:
            aardbeving_score = 3
        elif seismic_score > 4:
            aardbeving_score = 2
        else:
            aardbeving_score = 1
        
        if regen > 4:
            regen_score = 3
        elif regen > 3:
            regen_score = 2
        else:
            regen_score = 1
        
        total_score = (5*food_score + 3*lucht_score + 2*aardbeving_score + 4*regen_score)*10/42

    return round(total_score)


"""
Input:      seismische_score, giftige_gassen, aantal_aardbevingen
Output:     score van 1 (weinig) tot 10 (veel) hoe seismisch het is
"""
def bepaal_seismische_score(seismische_score, giftige_gassen, aantal_aardbevingen):
    if seismische_score[0]>8 or seismische_score[1]>8:
        ssm_score = 4
    elif seismische_score[0]>6 or seismische_score[1]>6:
        ssm_score = 3
    elif seismische_score[0]>4 or seismische_score[1]>4:
        ssm_score = 2
    else:
        ssm_score = 1
    
    if giftige_gassen > 0,5:
        gas_score = 4
    elif giftige_gassen > 0,4:
        gas_score = 3
    elif giftige_gassen > 0,3:
        gas_score = 2
    else:
        gas_score = 1

    if aantal_aarbevingen > 0,3:
        beving_score = 4
    elif aantal_aarbevingen > 0,2:
        beving_score = 3
    elif aantal_aarbevingen > 0,1:
        beving_score = 2
    else:
        beving_score = 1

    total_score = (beving_score + gas_score + ssm_score)*10/12
    return round(total_score)
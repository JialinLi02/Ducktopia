
import pandas as pd

data = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/Quentin_dataset.csv")
print(data)

import pandas as pd
import numpy as np

def aggregate_location_data(df):
    # Separate numerical, categorical, and tuple columns
    numerical_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(exclude=['number']).columns
    tuple_cols = [col for col in df.columns if isinstance(df[col].iloc[0], tuple)]

    # Group by 'Location' without sorting
    grouped = df.groupby('Location', sort=False)

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

agg_set = aggregate_location_data(data)
print(agg_set)
agg_set.to_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset_aggregated.csv", index=False)

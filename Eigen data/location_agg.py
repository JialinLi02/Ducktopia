
import pandas as pd

data = pd.read_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset.csv")
print(data)

import pandas as pd
import numpy as np

def aggregate_location_data(df):
    """
    Aggregates data by location. For numerical columns, it calculates the mean.
    For categorical columns, it takes the value from the first occurrence of each location.
    For tuple columns, it calculates the mean of each element in the tuple.

    Parameters:
        df (pd.DataFrame): The input DataFrame with a 'Location' column.

    Returns:
        pd.DataFrame: A new DataFrame with one row per location.
    """
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

agg_set = aggregate_location_data(data)
agg_set.to_csv("/Users/maxdesmedt/ducktopia_ae/Ducktopia/Eigen data/dataset_aggregated.csv", index=False)

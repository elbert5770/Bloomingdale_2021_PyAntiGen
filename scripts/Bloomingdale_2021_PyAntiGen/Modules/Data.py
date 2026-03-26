import pandas as pd
import os

def load_experiment1_data(data_path):
    experiment_path = os.path.join(data_path, 'PK_Predictions.csv')
    df = pd.read_csv(experiment_path)
    return df


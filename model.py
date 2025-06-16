import pandas as pd
import os

def load_absa_results():
    try:
        # Use path relative to this script's location
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "absa_ModelResults.xlsx")
        df = pd.read_excel(file_path)
        df.columns = [col.strip().lower() for col in df.columns]
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def get_platform_data(platform_name):
    df = load_absa_results()
    if "related_ofd" in df.columns:
        return df[df["related_ofd"].str.lower() == platform_name.lower()]
    return pd.DataFrame()

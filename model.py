import pandas as pd

def load_absa_results():
    try:
        df = pd.read_excel("absa_ModelResults.xlsx")
        return df
    except FileNotFoundError:
        return pd.DataFrame()

def get_platform_data(platform_name):
    df = load_absa_results()
    if "related_ofd" in df.columns:
        df.columns = [col.strip().lower() for col in df.columns]
        return df[df["related_ofd"].str.lower() == platform_name.lower()]
    return pd.DataFrame()

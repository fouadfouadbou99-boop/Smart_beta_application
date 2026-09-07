import pandas as pd

def calculate_scores(df):
    n=len(df)
    df=df.copy()
    df['ValueScore']=(df['PE'].rank(ascending=True)-1).rpow(0)
    return df

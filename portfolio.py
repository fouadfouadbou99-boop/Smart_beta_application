def build_portfolio(df):
    total=df['Composite'].sum()
    df['Weight']=df['Composite']/total
    return df

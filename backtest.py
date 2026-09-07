def backtest(df):
    return (df['Weight']*df['Perf']).sum()

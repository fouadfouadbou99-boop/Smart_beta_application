def composite_score(df):
    cols=['ValueScore','QualityScore','MomentumScore','LowVolScore']
    for c in cols:
        if c not in df.columns:
            df[c]=0
    df['Composite']=0.3*df['ValueScore']+0.3*df['QualityScore']+0.2*df['MomentumScore']+0.2*df['LowVolScore']
    return df.sort_values('Composite',ascending=False)

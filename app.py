import streamlit as st
import pandas as pd
from modules.factor_engine import calculate_scores
from modules.ranking import composite_score
from modules.portfolio import build_portfolio
from modules.backtest import backtest
from modules.excel_export import export_excel

st.set_page_config(page_title='Smart Beta Maroc', layout='wide')
st.title('Smart Beta Maroc')
file=st.file_uploader('Fichier Excel',type=['xlsx'])
if file:
    df=pd.read_excel(file,sheet_name=1)
    scores=calculate_scores(df)
    scores=composite_score(scores)
    port=build_portfolio(scores)
    st.dataframe(port)

import pandas as pd
import streamlit as st


st.title('🎈 Задачник')


DATA_PATH = 'https://raw.githubusercontent.com/jahongirka178/PhysRecSys/refs/heads/master/problems.csv'

df = pd.read_csv(DATA_PATH)

st.write(df['Task'].iloc[1])


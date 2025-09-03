import pandas as pd
import streamlit as st


st.title('📚 Готовимся к поступлению в ВУЗы')

DATA_PATH = 'https://raw.githubusercontent.com/jahongirka178/PhysRecSys/refs/heads/master/problems.csv'

df = pd.read_csv(DATA_PATH)

st.write(df['Task'].iloc[1])

# Sidebar
st.sidebar.header('Подбор задач:')

levels = df['Level'].unique().tolist()
levels.append('Разные')

level_input = st.sidebar.selectbox('Уровень задач', levels)
if level_input != 'Разные':
    number_of_tasks = st.sidebar.slider('Количество задач', 0, 20, 10)





import pandas as pd
import streamlit as st


st.title('📚 Готовимся к поступлению в ВУЗы')

DATA_PATH = 'https://raw.githubusercontent.com/jahongirka178/PhysRecSys/refs/heads/master/problems.csv'

df = pd.read_csv(DATA_PATH)
df['Level'] = df['Level'].replace({'А': 'A'})

st.write('''На реальном экзамене задачи делятся на следующие типы: \n
Часть 1 содержит 30 заданий (А1 – А30). К каждому заданию дается 4 варианта ответа, из которых правильный только один. \n
Часть 2 содержит 4 задания (В1 – В4), на которые следует дать краткий ответ в численном виде. \n
Часть 3 состоит из 6 заданий (С1 – С6), на которые требуется дать развернутый ответ. Необходимо записать законы физики, из которых выводятся требуемые для решения задачи соотношения. \n
''')
st.header('Начать решить можно в боковом меню. \n Желаем успехов!')

# Sidebar
st.sidebar.header('Подбор задач:')

levels = df['Level'].unique().tolist()
levels.append('Разные')

level_input = st.sidebar.selectbox('Уровень задач', levels)
if level_input != 'Разные':
    number_of_tasks = st.sidebar.slider('Количество задач', 0, 20, 10)







import pandas as pd
import streamlit as st
import json
import base64
from io import BytesIO
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = set(stopwords.words("russian"))
lemmatizer = WordNetLemmatizer()


def preprocess(text: str):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w.isalpha()]
    tokens = [w for w in tokens if w not in stop_words]
    return tokens

def build_model(df, column="Task"):
    documents = [TaggedDocument(preprocess(task), [i]) for i, task in enumerate(df[column])]
    model = Doc2Vec(vector_size=100, window=5, min_count=1, workers=4, epochs=40)
    model.build_vocab(documents)
    model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
    return model

def find_similar_task(df, model, user_text, column="Task", topn=1):
    user_vec = model.infer_vector(preprocess(user_text))
    task_vecs = [model.infer_vector(preprocess(task)) for task in df[column]]
    sims = cosine_similarity([user_vec], task_vecs)[0]
    best_idx = sims.argsort()[::-1][:topn]
    return df[column].iloc[best_idx].tolist()

def show_images(row):
    img_list = json.loads(row)
    for img_b64 in img_list:
        img_bytes = base64.b64decode(img_b64)
        img = Image.open(BytesIO(img_bytes))
        st.image(img)


def show_A(df):
    k = 0
    for _, row in df.iterrows():
        k = k + 1
        st.subheader(f"Задача №{k}: \n {row['Task']}")
        try:
            choices = json.loads(row["Choices"])
        except Exception:
            choices = []
        show_images(row['Images'])
        answer = st.radio(
            "Выберите ответ:",
            choices,
            index=None,
            key=f"task_{k}"
        )


def show_B(df):
    k = 0
    for i, row in df.iterrows():
        k = k + 1
        st.subheader(f"Задача №{k}: \n {row['Task']}")
        show_images(row['Images'])
        answer = st.text_input("Введите ответ:", key=f"answer_{i}")


def show_C(df):
    k = 0
    for i, row in df.iterrows():
        k = k + 1
        st.subheader(f"Задача №{k}: \n {row['Task']}")
        show_images(row['Images'])
        answer = st.text_input("Введите ответ:", key=f"answer_{i}")


st.title('📚 Готовимся к поступлению в ВУЗы')

DATA_PATH = 'https://raw.githubusercontent.com/jahongirka178/PhysRecSys/refs/heads/master/problems.csv'

df = pd.read_csv(DATA_PATH)
df['Level'] = df['Level'].replace({'А': 'A'})
df['Level'] = df['Level'].replace({'С': 'C'})


st.write('''На реальном экзамене задачи делятся на следующие типы: \n
Часть 1 содержит 30 заданий (А1 – А30). К каждому заданию дается 4 варианта ответа, из которых правильный только один. \n
Часть 2 содержит 4 задания (В1 – В4), на которые следует дать краткий ответ в численном виде. \n
Часть 3 состоит из 6 заданий (С1 – С6), на которые требуется дать развернутый ответ. Необходимо записать законы физики, из которых выводятся требуемые для решения задачи соотношения. \n
''')
st.header('Ниже перечислены задачи. \n Желаем успехов!')

# Sidebar
st.sidebar.header('Подбор задач:')

levels = df['Level'].unique().tolist()
levels.append('Разные')

level_input = st.sidebar.selectbox('Уровень задач', levels)
if level_input != 'Разные':
    number_of_tasks = st.sidebar.slider('Количество задач', 0, 20, 10)

if level_input == 'A':
    st.subheader(f'Задачи уровня A - {number_of_tasks} штук')
    a_tasks = df[df['Level'] == 'A'].sample(int(number_of_tasks))
    show_A(a_tasks)

if level_input == 'B':
    st.subheader(f'Задачи уровня B - {number_of_tasks} штук')
    b_tasks = df[df['Level'] == 'B'].sample(int(number_of_tasks))
    show_B(b_tasks)

if level_input == 'C':
    st.subheader(f'Задачи уровня C - {number_of_tasks} штук')
    c_tasks = df[df['Level'] == 'C'].sample(int(number_of_tasks))
    show_C(c_tasks)

if level_input == 'Разные':
    st.subheader(f'Задачи уровня A - 15 штук.')
    a_tasks = df[df['Level'] == 'A'].sample(15)
    show_A(a_tasks)

    st.subheader(f'Задачи уровня B - 10 штук.')
    b_tasks = df[df['Level'] == 'B'].sample(10)
    show_B(b_tasks)

    st.subheader(f'Задачи уровня C - 5 штук.')
    c_tasks = df[df['Level'] == 'C'].sample(5)
    show_C(c_tasks)


if st.button("Проверить"):
    st.write("Идёт подсчёт...")


st.header('Похожие задачи.')
st.sidebar.header('Подбор похожих задач:')
answer = st.sidebar.text_area(
    "Ключевые слова или целая задача",
    height=200
)

if st.sidebar.button("Найти"):
    model = build_model(df)
    result = find_similar_task(df, model, answer, topn=5)
    st.dataframe(result)


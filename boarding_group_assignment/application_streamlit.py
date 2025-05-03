import pandas as pd
import streamlit as st

from problem import CarGropProblem


def preprocess(students, cars):
    """ UploadFile(csv) -> pd.DataFrame """
    df_students = pd.read_csv(students)
    df_cars = pd.read_csv(cars)
    return df_students, df_cars


def convert_to_csv(df):
    """ pd.DataFrame -> csv """
    return df.to_csv().encode('utf-8')


col1, col2 = st.columns(2)

with col1:
    students = st.file_uploader('学生 Data', type='csv')
    cars = st.file_uploader('車 Data', type='csv')

    if students is not None and cars is not None:
        if st.button('最適化を実行'):
            df_students, df_cars = preprocess(students, cars)

            df_solution = CarGropProblem(df_students, df_cars).solve()

            with col2:
                st.write('#### 最適化結果')
                csv = convert_to_csv(df_solution)
                st.download_button(
                    'Press to Download',
                    csv,
                    'solution.csv',
                    'text/csv',
                    key='download-csv'
                )
                st.write(df_solution)

from fastapi import FastAPI
import pandas as pd
from pydantic import BaseModel
import uvicorn
from typing import List

from problem import CarGropProblem

app = FastAPI()


def preprocess(students, cars):
    """ Request Data を受取、DataFrame に変換する関数 """
    df_students = pd.DataFrame(students)
    df_cars = pd.DataFrame(cars)
    return df_students, df_cars


def postprocess(df_solution):
    """ DataFrame を csv に変換する関数 """
    csv_solution = df_solution.to_dict(orient='records')
    return csv_solution


class Student(BaseModel):
    student_id: int
    grade: int
    gender: int
    license: int


class Car(BaseModel):
    car_id: int
    capacity: int


class Solution(BaseModel):
    student_id: int
    car_id: int


@app.post('/api')
def solve(students: List[Student], cars: List[Car]) -> List[Solution]:
    """ 最適化問題を解く API 用の関数 """
    # 1. Request 受信
    students = [s.dict() for s in students]
    cars = [c.dict() for c in cars]
    df_students, df_cars = preprocess(students, cars)
    # 2. 最適化実行
    df_solution = CarGropProblem(df_students, df_cars).solve()
    # 3. Response 返信
    response = postprocess(df_solution)
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

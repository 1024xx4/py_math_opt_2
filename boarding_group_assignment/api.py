# Libraries
from flask import Flask, request, make_response
import pandas as pd

from problem import CarGropProblem

# Create a Flask Application
app = Flask(__name__)


def preprocess(request):
    """ Request Data を受け取り、DataFrame に変換する関数"""
    # 各 File を取得する
    students = request.files['students']
    cars = request.files['cars']
    # pandas で読み込む
    df_students = pd.read_csv(students)
    df_cars = pd.read_csv(cars)
    return df_students, df_cars


def postprocess(df_solution):
    """ DataFrame を csv に変換する関数 """
    csv_solution = df_solution.to_csv(index=False)
    response = make_response()
    response.data = csv_solution
    response.headers['Content-Type'] = 'text/csv'
    return response


# 最適化問題を解く API 用の関数
@app.route('/api', methods=['POST'])
def solve():
    # Request の受信
    df_students, df_cars = preprocess(request)

    # 最適化実行
    df_solution = CarGropProblem(df_students, df_cars).solve()

    # Response 実行
    response = postprocess(df_solution)
    return response

from flask import Flask, make_response, redirect, render_template, request
import pandas as pd

from problem import CarGropProblem

app = Flask(__name__)


def check_request(request):
    """ Request に学生 Data と車 Data が含まれているか確認する関数"""
    # 各 File を取得する
    students = request.files['students']
    cars = request.files['cars']

    # File が選択がされているか確認
    if students.filename == '':
        return False  # 学生 Data が選ばれていません
    if cars.filename == '':
        return False  # 車 Data が選ばれていません

    return True


def preprocess(request):
    """ Request Data を受取、DataFrame に変換する関数"""
    students = request.files['students']
    cars = request.files['cars']
    df_students = pd.read_csv(students)
    df_cars = pd.read_csv(cars)

    return df_students, df_cars


def postprocess(df_solution):
    """ 最適化結果を HTML 形式に変換する関数 """
    html_solution = df_solution.to_html(index=False, header=True)
    return html_solution


@app.route('/', methods=['GET', 'POST'])
def solve():
    """ 最適化の実行と結果の表示を行う関数 """
    # TOP Page を表示する(GET)
    if request.method == 'GET':
        return render_template('index.html', solution_html=None)

    # POST Request である「最適化を実行」Button が押下された時に実行
    # Data が Upload されているか check する。されていなければ元の Page へ redirect.
    if not check_request(request):
        return redirect(request.url)

    df_students, df_cars = preprocess(request)  # 前処理（Data 読み込み）
    df_solution = CarGropProblem(df_students, df_cars).solve()  # 最適化実行
    html_solution = postprocess(df_solution)
    return render_template('index.html', solution_html=html_solution)  # 後処理（最適化結果を HTML に表示できる形式にする）


@app.route('/download', methods=['POST'])
def download():
    """ Request に含まれる HTML の表形式 Data を csv形式にし変換して DL する関数 """
    html_solution = request.form.get('solution_html')
    df_solution = pd.read_html(html_solution)[0]
    csv_solution = df_solution.to_csv(index=False)
    response = make_response()
    response.data = csv_solution
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=solution.csv'
    return response

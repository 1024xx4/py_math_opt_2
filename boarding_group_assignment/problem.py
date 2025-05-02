# problem.py
import pandas as pd
import pulp


class CarGropProblem:
    """学生の乗車グループ分け問題を解く Class"""

    def __init__(self, df_students, df_cars, name='ClubCarProblem'):
        # Initalize Methodes
        self.df_students = df_students
        self.df_cars = df_cars
        self.name = name
        self.prob = self._formulate()

    def _formulate(self):
        # 学生の乗車グループ分け問題（0-1整数計画問題）の Instance 作成
        prob = pulp.LpProblem('ClubCarProblem', pulp.LpMinimize)  # Generate Instance.

        # List
        students = df_students['student_id'].tolist()  # 学生 List
        cars = df_cars['car_id'].tolist()  # 車 List
        grades = list(range(1, 5, 1))
        students_cars = [(student, car) for student in students for car in cars]  # 学生の車の Pair の List
        licensers = df_students.loc[df_students['license'] == 1, 'student_id']  # 免許を持っている学生の List
        students_grades = {grade: df_students.loc[df_students['grade'] == grade, 'student_id'] for grade in
                           grades}  # 学年が grade の学生 List
        students_male = df_students.loc[df_students['gender'] == 0, 'student_id']
        students_female = df_students.loc[df_students['gender'] == 1, 'student_id']

        # 定数
        # 車の乗車定員の定数
        CAR_CAPACITY = df_cars['capacity'].tolist()

        # 変数
        # 学生をどの車に割り当てるかを変数として定義
        x = pulp.LpVariable.dicts('x', students_cars, cat='Binary')

        # 制約
        # 1. 各学生を１つの車に割り当てる
        for student in students:
            prob += pulp.lpSum([x[student, car] for car in cars]) == 1

        # 2. 法規則に関する制約: 各車には乗車定員より多く乗ることができない
        for car in cars:
            prob += pulp.lpSum([x[student, car] for student in students]) <= CAR_CAPACITY[car]

        # 3. 法規制に関する制約: 各車に Driver を１人以上割り当てる
        for car in cars:
            prob += pulp.lpSum([x[licenser, car] for licenser in licensers]) >= 1

        # 4. 懇親を目的とした制約: 各車に各学年の学生を１人以上割り当てる
        for car in cars:
            for car in cars:
                for grade in grades:
                    prob += pulp.lpSum([x[student_grade, car] for student_grade in students_grades[grade]]) >= 1

        # 5. Gender Balance を考慮した制約: 各車に男性を１人以上割り当てる
        for car in cars:
            prob += pulp.lpSum([x[student_male, car] for student_male in students_male]) >= 1

        # 6. Gender Balance を考慮した制約: 各車に女性を１人以上割り当てる
        for car in cars:
            prob += pulp.lpSum([x[student_female, car] for student_female in students_female]) >= 1

        # 最適化後に利用する Data を返却
        return {'prob': prob, 'variable': {'x': x}, 'list': {'students': students, 'cars': cars}}

    def solve(self):
        # 最適化問題を解く Methode
        status = self.prob['prob'].solve()  # 問題を解く

        # 最適化結果を格納
        x = self.prob['variable']['x']
        students = self.prob['list']['students']
        cars = self.prob['list']['cars']
        car2students = {car: [student for student in students if x[student, car].value() == 1] for car in cars}
        student2car = {student: car for car, students in car2students.items() for student in students}
        df_solution = pd.DataFrame(list(student2car.items()), columns=['student_id', 'car_id'])

        return df_solution


if __name__ == '__main__':
    # Data の読み込み
    df_students = pd.read_csv('resource/students.csv')
    df_cars = pd.read_csv('resource/cars.csv')

    # 数理 Model Instance の作成
    prob = CarGropProblem(df_students, df_cars)

    # 求解
    df_solution = prob.solve()

    # 結果の表示
    print(f'Solution: \n {df_solution}')

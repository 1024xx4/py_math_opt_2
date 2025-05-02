import requests

# API の Endpoint
url = 'http://127.0.0.1:5000/api'

# Request で渡す Data
files = {'students': open('resource/students.csv'), 'cars': open('resource/cars.csv')}

# POST Request
response = requests.post(url, files=files)

# 結果の保存
with open('resource/solution_requests.csv', 'w') as f:
    f.write(response.text)

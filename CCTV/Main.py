import subprocess
from flask import Flask, render_template, request
import cx_Oracle as db
import matplotlib.pyplot as plt
import io
import base64
import DAO as dao

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cctv')
def Detect():
    result = subprocess.run(['python', r'C:\\project\\CCTV\\Detect.py'], capture_output=True, text=True)
    if result.returncode != 0:
        # 스크립트 실행 중 에러 발생
        return f"Error: {result.stderr}"
    return result.stdout

@app.route('/chart')
def chart():
    return render_template('chart.html', plot_url=dao.plot())

@app.route('/dashboard')
def showdashboard():
    return render_template('ChartDashboard.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # POST 요청으로부터 데이터를 가져옵니다.
    startDatetime = request.form['startDatetime']
    endDatetime = request.form['endDatetime']
    minAge = request.form['minAge']
    maxAge = request.form['maxAge']
    gender = request.form['gender']

    # 가져온 데이터를 딕셔너리 형태러 저장
    params = {
        'startDatetime' : startDatetime,
        'endDatetime' : endDatetime,
        'minAge' : minAge,
        'maxAge' : maxAge,
        'gender' : gender
    }

    # 가져온 데이터를 처리하거나 응답을 생성합니다.
    date_count_url = dao.date_count(params)
    return render_template('chart.html', date_count_url=date_count_url)

if __name__ == '__main__':
    app.run(debug=True)


import subprocess
from flask import Flask, render_template
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

if __name__ == '__main__':
    app.run(debug=True)


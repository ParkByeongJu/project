import DataBase as db
import matplotlib.pyplot as plt
import io
import base64
import font as ft

def date_count(params):
    cursor, connection = db.db()
    font = ft.font()
    # plt.rc("font", family=font)
    # 쿼리 실행
    query = """SELECT 
                    TO_CHAR(detect_time, 'YYYY-MM-DD') AS detect_date, 
                    COUNT(*) AS daily_count 
                FROM 
                    test
                WHERE 
                    TO_CHAR(detect_time, 'YYYY-MM-DD') BETWEEN :start_date AND :end_date
                GROUP BY 
                    TO_CHAR(detect_time, 'YYYY-MM-DD')
                ORDER BY 
                    detect_date"""
    cursor.execute(query, start_date=params['startDatetime'], end_date=params['endDatetime'])

    # 데이터 가져오기
    data = cursor.fetchall()

    # 데이터 분리
    dates = [row[0] for row in data]
    counts = [row[1] for row in data]

    # 막대 그래프 생성
    plt.rcParams['font.family'] = font
    plt.rcParams['axes.unicode_minus'] =False
    plt.figure(figsize=(6, 4))
    plt.plot(dates, counts, marker='o')
    plt.xlabel('날짜')
    plt.ylabel('방문 인원')
    plt.title('날짜별 방문 인원수')

    # 이미지를 바이트스트림으로 변환
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    date_count_url = base64.b64encode(img.getvalue()).decode()

    # 연결 종료
    cursor.close()
    connection.close()

    # HTML에 이미지를 전달
    return date_count_url

def time_count(params):
    cursor, connection = db.db()
    font = ft.font()
    query = """SELECT 
                    gender,
                    TO_CHAR(detect_time, 'HH24') AS detect_hour,
                    COUNT(*) AS count
                FROM
                    test
                GROUP BY
                    TO_CHAR(detect_time, 'HH24'),
                    gender
                ORDER BY
                    detect_hour;"""
    cursor.execute(query)
import DataBase as db
import matplotlib.pyplot as plt
import io
import base64

def plot():
    cursor, connection = db.db()
    # 쿼리 실행
    query = """SELECT 
                    TO_CHAR(detect_time, 'YYYY-MM-DD') AS detect_date, 
                    COUNT(*) AS daily_count 
                FROM 
                    test
                WHERE 
                    TO_CHAR(detect_time, 'YYYY-MM-DD') BETWEEN '2023-10-27' AND '2023-10-29'
                GROUP BY 
                    TO_CHAR(detect_time, 'YYYY-MM-DD')
                ORDER BY 
                    detect_date"""
    cursor.execute(query)

    # 데이터 가져오기
    data = cursor.fetchall()

    # 데이터 분리
    dates = [row[0] for row in data]
    counts = [row[1] for row in data]

    # 막대 그래프 생성
    plt.figure(figsize=(6, 4))
    plt.bar(dates, counts)
    plt.xlabel('Detect Date')
    plt.ylabel('Daily Count')
    plt.title('Number of detected faces by date')

    # x축 정렬
    plt.xticks(rotation=45)

    # 이미지를 바이트스트림으로 변환
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    # 연결 종료
    cursor.close()
    connection.close()

    # HTML에 이미지를 전달
    return plot_url


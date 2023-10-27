import cx_Oracle as db
import matplotlib.pyplot as plt

# Oracle 데이터베이스에 연결하기 위한 정보
dsn = db.makedsn(host='localhost', port=1521, service_name='xe')
user = 'hr'
password = 'hr'

# 데이터베이스 연결
connection = db.connect(user=user, password=password, dsn=dsn)
cursor = connection.cursor()

# 쿼리 실행
query = """
SELECT
TO_CHAR(detect_time, 'YYYY-MM-DD') AS detect_date,
COUNT(*) AS daily_count
FROM
test
WHERE
TO_CHAR(detect_time, 'YYYY-MM-DD') BETWEEN '2023-10-27' AND '2023-10-29'
GROUP BY
TO_CHAR(detect_time, 'YYYY-MM-DD')
ORDER BY
detect_date
"""
cursor.execute(query)

# 데이터 가져오기
data = cursor.fetchall()
print(data)

# 데이터 분리 및 날짜 순서로 정렬
data.sort(key=lambda x: x[0])
dates = [row[0] for row in data]
counts = [row[1] for row in data]

# 막대 그래프 생성
plt.figure(figsize=(10, 6))
plt.bar(dates, counts)
plt.xlabel('Date')
plt.ylabel('Count')
plt.title('Number of daily detections')

# x축 정렬
plt.xticks(dates, rotation=45)
plt.show()

# 연결 종료
cursor.close()
connection.close()

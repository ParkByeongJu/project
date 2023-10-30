import cv2
import numpy as np
import DataBase as db
import matplotlib.pyplot as plt
from datetime import datetime
import io
import base64

def heatMap(params):
    cursor, connection = db.db()
    # 기본 쿼리 문자열
    base_query = "SELECT start_x, start_y, end_x, end_y FROM detected_faces"

    # 가능한 모든 연령 범위
    age_ranges = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']

    # 선택한 연령 범위에 따른 조건 추가
    if params['minAge'] is not None and params['maxAge'] is not None:
        min_index = age_ranges.index(params['minAge'])
        max_index = age_ranges.index(params['maxAge'])
        selected_ranges = age_ranges[min_index : max_index + 1]
        
        rows = []
        for age_range in selected_ranges:
            conditions = []

            # 성별 조건 추가
            if params['gender'] in ['Male', 'Female']:
                conditions.append(f"gender = '{params['gender']}'")

            # 연령 조건 추가
            conditions.append(f"age = '{age_range}'")

            # 날짜 조건 추가
            if params['startDatetime'] is not None and params['endDatetime'] is not None:
                startDate = datetime.strptime(params['startDatetime'], "%Y-%m-%dT%H:%M").strftime("%d/%m/%Y")
                endDate = datetime.strptime(params['endDatetime'], "%Y-%m-%dT%H:%M").strftime("%d/%m/%Y")
                conditions.append(f"TRUNC(detect_time) BETWEEN TO_DATE('{startDate}', 'DD/MM/YYYY') AND TO_DATE('{endDate}', 'DD/MM/YYYY')")
            
            # 조건이 하나 이상 있는 경우, WHERE 절 추가
            if conditions:
                query = base_query + " WHERE " + " AND ".join(conditions)
            else:
                query = base_query

            cursor.execute(query)
            print(query)
            rows.extend(cursor.fetchall())
        
        print(rows)
    

    # 원본 이미지 읽기
    # image = cv2.imread('D:\\project\\CCTV\\image.png')
    image = cv2.imread('C:\\project\\CCTV\\image.png')

    # 이미지의 높이와 너비를 frame_height와 frame_width에 대입
    frame_height, frame_width = image.shape[:2]
    heatmap = np.zeros((frame_height, frame_width))
    print(f"Image width: {frame_width}, Image height: {frame_height}")  # 이미지 크기 출력

    for row in rows:
        if None in row:
            continue
        start_x, start_y, end_x, end_y = row
        if end_x >= frame_width or end_y >= frame_height:
            print(f"Out of bounds: end_x = {end_x}, end_y = {end_y}")
            continue
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                heatmap[y, x] += 1000  # y, x 순서에 주의하세요.

    # 히트맵 정규화
    # heatmap = np.log(heatmap + 1e-10) 
    heatmap = heatmap / np.max(heatmap) * 255

    # 가우시안 필터 적용
    heatmap = cv2.GaussianBlur(heatmap, (105, 105), 0)

    # 히트맵을 원본 이미지 크기에 맞게 변경
    heatmap_resized = cv2.resize(heatmap, (frame_width, frame_height))

    # 히트맵을 BGR 형태로 변경
    heatmap_color = cv2.applyColorMap(np.uint8(heatmap_resized), cv2.COLORMAP_JET)

    # 원본 이미지에 히트맵 추가
    image_heatmap = cv2.addWeighted(image, 0.7, heatmap_color, 0.3, 0)

    # 원본 이미지, 히트맵, 히트맵을 적용한 이미지 표시
    img = io.BytesIO()
    plt.imsave(img, cv2.cvtColor(image_heatmap, cv2.COLOR_BGR2RGB), format='png')
    img.seek(0)
    heatmap_url = base64.b64encode(img.getvalue()).decode()

    return heatmap_url

# create_heatmap_on_image('C:\\project\\CCTV\\image.png')
# create_heatmap_on_image('D:\\project\\CCTV\\image.png')
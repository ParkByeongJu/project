import cv2
import numpy as np
import DataBase as db


def create_heatmap_on_image(image_path):
    cursor, connection = db.db()
    cursor.execute("SELECT start_x, start_y, end_x, end_y FROM detected_faces")
    rows = cursor.fetchall()
    

    # 원본 이미지 읽기
    image = cv2.imread("C:\\project\\CCTV\\image.png")

    # 이미지의 높이와 너비를 frame_height와 frame_width에 대입
    frame_height, frame_width = image.shape[:2]
    heatmap = np.zeros((frame_height, frame_width))
    print(f"Image width: {frame_width}, Image height: {frame_height}")  # 이미지 크기 출력

    max_start_x = max([row[0] for row in rows if row[0] is not None])
    max_start_y = max([row[1] for row in rows if row[1] is not None])
    max_end_x = max([row[2] for row in rows if row[2] is not None])
    max_end_y = max([row[3] for row in rows if row[3] is not None])

    print(f"Max start_x: {max_start_x}, Max start_y: {max_start_y}, Max end_x: {max_end_x}, Max end_y: {max_end_y}")  # 얼굴 좌표의 최대값 출력
    for row in rows:
        if None in row:
            continue
        start_x, start_y, end_x, end_y = row
        if end_x >= frame_width or end_y >= frame_height:
            print(f"Out of bounds: end_x = {end_x}, end_y = {end_y}")
            continue
        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                heatmap[x, y] += 1000

    # 히트맵 정규화
    heatmap = np.log(heatmap + 1e-10) 
    heatmap = heatmap / np.max(heatmap) * 255
    # print(heatmap)

    # 히트맵을 원본 이미지 크기에 맞게 변경
    heatmap_resized = cv2.resize(heatmap, (frame_width, frame_height))

    # 히트맵을 BGR 형태로 변경
    heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)

    # 원본 이미지에 히트맵 추가
    image_heatmap = cv2.addWeighted(image, 0.7, heatmap_color, 0.3, 0)

    # 원본 이미지, 히트맵, 히트맵을 적용한 이미지 표시
    cv2.imshow('Image with Heatmap', image_heatmap)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

create_heatmap_on_image('C:\\project\\CCTV\\image.png')
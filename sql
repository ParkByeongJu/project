CREATE TABLE detected_faces (
    face_id NUMBER,
    gender VARCHAR2(10),
    age VARCHAR2(10),
    start_x NUMBER,
    start_y NUMBER,
    end_x NUMBER,
    end_y NUMBER,
    detect_time TIMESTAMP
);

select * from detected_faces;
------------------------------------
drop table detected_faces;
------------------------------------
SELECT * 
  FROM detected_faces 
 WHERE TO_CHAR(detect_time, 'YYYY-MM-DD') = '2023-10-27' 
   AND gender = 'Male';
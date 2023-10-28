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

create table test (
    gender VARCHAR2(10),
    age VARCHAR2(10),
    detect_time TIMESTAMP
);

select * from test;

INSERT INTO test (gender, age, detect_time) VALUES ('Male', '(25, 32)', '23/10/29 19:42:05'); 
commit;
------------------------------------
drop table test;
------------------------------------
SELECT * 
  FROM detected_faces 
 WHERE TO_CHAR(detect_time, 'YYYY-MM-DD') = '2023-10-27' 
   AND gender = 'Male';
   
   
--날짜별
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
    detect_date;
    
--시간대별
SELECT 
    gender,
    TO_CHAR(detect_time, 'HH24') AS detect_hour,
    COUNT(*) AS count
FROM
    test
GROUP BY
    TO_CHAR(detect_time, 'HH24'),
    gender
ORDER BY
    detect_hour;
    
-- 나이대별
SELECT 
    gender,
    age,
    COUNT(*) AS count
FROM
    test
GROUP BY
    gender,
    age
ORDER BY
    age, gender;

-- 범위를 지정해주면 통합 남여 구분
select
    gender,
    count(*) as count
from test
group by gender;

SELECT
        TO_CHAR(detect_time, 'YY/MM/DD') AS detect_date,
        COUNT(*) AS daily_count
        FROM
        test
        WHERE
        TO_CHAR(detect_time, 'YY/MM/DD') BETWEEN '23/10/27' AND '23/10/29'
        GROUP BY
        TO_CHAR(detect_time, 'YY/MM/DD')
        ORDER BY
        detect_date;
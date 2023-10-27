import cx_Oracle as db_module

def db():
    # Oracle 데이터베이스에 연결하기 위한 정보
    dsn = db_module.makedsn(host='localhost', port=1521, service_name='xe')
    user = 'hr'
    password = 'hr'

    # 데이터베이스 연결
    connection = db_module.connect(user=user, password=password, dsn=dsn)
    cursor = connection.cursor()
    return cursor, connection
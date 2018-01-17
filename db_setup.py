#coding:utf-8
import pymysql
import dbconfig
connection = pymysql.connect(host='localhost',
                             user=dbconfig.db_user,
                             passwd=dbconfig.db_password)
# 这也是异常处理，无论try怎么都会执行finally的语句，即关闭连接
try:
    # 异常处理，with后面接的是要异常处理的语句，它返回的值在as后面接受。如果前面语句出错，会有异常处理的
    with connection.cursor() as cursor:
        sql = 'CREATE DATABASE IF NOT EXISTS crimemap'
        cursor.execute(sql)
        sql = '''
        CREATE TABLE IF NOT EXISTS crimemap.crimes (
        id int NOT NULL AUTO_INCREMENT,
        latitude FLOAT(10,6),
        longitude FLOAT(10,6),
        date DATETIME,
        category VARCHAR(50),
        description VARCHAR(1000),
        updated_at TIMESTAMP,
        PRIMARY KEY(id)
        )'''
        cursor.execute(sql)
        # 记住一定要commit
        connection.commit()
finally:
    connection.close()


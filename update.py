import pymysql
import pandas as pd


sql="update xiaoqing2024 join(select id from xiaoqing2024 where NO = '{}') as sub ON xiaoqing2024.id = sub.id SET xiaoqing2024.price = {};"
# sql_="insert into xiaoqing2024(NO,NAME,speces,brand,unit,price) values(%s,%s,%s,%s,%s,%s)"
sql_="insert into xiaoqing2024(NO,NAME,speces,brand,unit,price) select %s,%s,%s,%s,%s,%s where not exists (select 1 from xiaoqing2024 where NO = %s and price =%s);"
sql_1 = "select NO,NAME,speces,brand,unit,price from xiaoqing2024;"


def connect_db():
    try:
        db =pymysql.connect(host='localhost',
                    user='root',
                    password='root',
                    database='user')
        cursor = db.cursor()
        return db,cursor
    except pymysql.MySQLError as e:
        return None, None

def update(file1):
    db, cursor = connect_db()  # 每次更新时重新连接数据库
    if db is None or cursor is None:
        return '数据库连接失败'
    try:
        df_ = pd.read_excel(file1, usecols='C:H',skiprows=1 ,names=None)
        # df_replaced = df.replace(to_replace=pd.NA, value='NULL')
        df_replaced_=df_.fillna('NULL')
        df_li_ = df_replaced_.values.tolist()
        # print(df_li_)

        mysql_data = []
        mysql_NO = []

        cursor.execute(sql_1)
        result = cursor.fetchall()
        for i in result:
            a=list(i)
            mysql_data.append(a)
            mysql_NO.append(a[0])


        for i in df_li_:
            i_tuple = tuple(i)
            if i not in mysql_data:
                if i[0] not in mysql_NO and i[0] != 'NULL': 
                    
                    i_tuple=i_tuple+(i_tuple[0],i_tuple[5])
                                      
                    cursor.execute(sql_,i_tuple)
                
                    db.commit()
                else:                   
                    cursor.execute(sql.format(i_tuple[0],i_tuple[5]))
                    db.commit()
            else:               
                return 
        return 'update is over'
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        cursor.close()
        db.close()





# file1 = 'D:/2025-9月数据库.xlsx'
# update(file1)

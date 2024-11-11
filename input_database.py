import pymysql
import pandas as pd

db =pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='user')
cursor = db.cursor()
sql="insert into xiaoqing2024(NO,NAME,speces,brand,unit,price) values(%s,%s,%s,%s,%s,%s)"

# file1='D:\晓庆2024数据库.xlsx'
# file='D:\\other.xlsx'

def input(file):
  try:
      df = pd.read_excel(file, usecols='C:H', names=None)
      df_replaced = df.replace(to_replace=pd.NA, value='NULL')
      df_li = df_replaced.values.tolist()
    #  print(df_li)

      for row in df_li:
        cursor.execute(sql, tuple(row))
      # 提交事务
        db.commit()
  except Exception as e:
      # 打印异常信息
      print(f"An error occurred: {e}")
      # 发生错误时回滚
      db.rollback()
  finally:
      # 关闭数据库连接
      db.close()
      return
input('D:\\2024-11月数据库（降价后）.xlsx')


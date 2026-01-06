import pymysql
import pandas as pd
import time
db =pymysql.connect(host='localhost',
                     user='root',
                     password='root',
                     database='user')
cursor = db.cursor()
def check(file):
  sql='select * from xiaoqing2024 where NO in {} and price in {} order by NO;'
  try:
    # df = pd.read_excel(file, sheet_name='黄岛总表',usecols='B,G', nrows=20, skiprows=1, names=None)
    df = pd.read_excel(file, sheet_name='图示',usecols='B,G', nrows=20,  names=None)
    df_replaced=df.fillna('NULL')
    df_li = df_replaced.values.tolist()

    NO = []
    price = []

    for row in df_li:
        NO.append(row[0])
        price.append(row[1])  

    cursor.execute(sql.format(tuple(NO),tuple(price)))
    
    results = cursor.fetchall()
    # df_results = pd.DataFrame(results)
    # print(df_results)
    return results

  except Exception as e:
      print(f"An error occurred: {e}")
      db.rollback()




# check("D:/2025-08月电算mro部品申请.xlsx")


#  Querying Data Using Connector/Python
import mysql.connector

from setting import password

cnx = mysql.connector.connect(user='root', password=password, host='127.0.0.1', database='pchome_airfryer')
cursor = cnx.cursor(dictionary=True)                  # 若加上字典，下面直接列印就是字典了

# query = ("SELECT * FROM product "
#          "WHERE price >= 15980")

query = ("SELECT * FROM airfryer "
         "WHERE name LIKE '%飛利浦%'")                   # name裡面包含... 用 LIKE '%ps5%' ，(第一個%代表這字串前面可以有東西，第二個後面可以有東西，若第一個沒寫，代表得PS5開頭)
                                                      # 以及要住要"" 跟'' 做為區別，避免開關掉

cursor.execute(query)

# for (name, price) in cursor:
#     print(name)
#     print(price)

for row in cursor:
  # print(row)
  print(row['name'], row['price'], row['originprice'])

cursor.close()
cnx.close()
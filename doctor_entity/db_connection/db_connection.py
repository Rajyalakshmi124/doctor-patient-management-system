import mysql.connector

#db connection 
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root"
)
 
print(mydb)

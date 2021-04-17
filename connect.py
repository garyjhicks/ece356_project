import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="MLB"
)

mycursor = mydb.cursor()


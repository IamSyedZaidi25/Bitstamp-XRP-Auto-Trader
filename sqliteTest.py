import sqlite3
import bcrypt
import getpass

conn = sqlite3.connect("mydatabase.db")
cursor = conn.cursor()

username = input("Please input your username: ")

cursor.execute("SELECT * FROM ACCOUNT WHERE user="+"'"+username+"'")

accountData = cursor.fetchall()

while len(accountData) < 1:
	username = input("Incorrect username, please re-enter: ")
	cursor.execute("SELECT * FROM ACCOUNT WHERE user="+"'"+username+"'")
	accountData = cursor.fetchall()

password = bytes(accountData[0][1],'utf-8')

passIn = getpass.getpass(prompt="Please enter password to unlock: ")
passIn = bytes(passIn, 'utf-8')
passInHashed = bcrypt.hashpw(passIn, password)

while passInHashed != password:
	passIn = getpass.getpass(prompt="Incorrect password, please re-enter: ")
	passIn = bytes(passIn, 'utf-8')
	passInHassed = bcrypt.hashpw(passIn, password)



print("Unlock successful...")

conn.commit()
cursor.close()
conn.close()

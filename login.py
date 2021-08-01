#import mysql.connector
import eel
#import MySQLdb
from database import *

session = {}

conn = create_connection()
cursor = conn.cursor()

@eel.expose
def teacher_login(user_name,password):
	data = []
	sql = "SELECT * from teacher_login WHERE user_name= ? AND password = ?"
	val = [user_name,password]
	cursor.execute(sql,val)
	result = cursor.fetchall()
	#print(result[0][1])
	if len(result)==1:
		global session
		session['auth'] = True
		session['user_name'] = result[0][1]
		eel.login_success("dashboard.html")

	else:
		eel.login_error('Invalid Username or Password')
	##print(mycursor)
	"""
	for x in mycursor:
		if user_name in x:
			if password in x:
				global session
				session['auth'] = True
				session['user_name'] = user_name
				#print(session)
				eel.login_success("dashboard.html")
			else:
				eel.login_error('Invalid Password')
				print('invalid password')
		else:
			eel.login_error('Invalid Username')
			#print('invalid user_name')
	"""
@eel.expose
def logout():
	global session
	session['auth'] = False
	session['user_name'] = ""
	eel.logout()

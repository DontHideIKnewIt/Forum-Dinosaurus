from flask import Flask, redirect, render_template, session, url_for, request
import sqlite3 as sql
app = Flask(__name__)
app.secret_key = 'any random string'

@app.route('/')
def home():
   con = sql.connect("database.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("SELECT * FROM thread")
   rows = cur.fetchall()
   con.close()
   return render_template('index.html',rows=rows)
	

@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/insert')
def insert():
	return render_template('insert.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/system', methods = ['POST','GET'])
def system():

   con = sql.connect("database.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   if request.form.get('register',None)!=None:
	Email = request.form['email']
	Password = request.form['password']
	cur.execute("select MAX(userId) from users")
  	row = cur.fetchone()
	max = row[0]+1
	try:
		cur.execute("INSERT INTO users (userid, email, password) VALUES (?,?,?)",(max,Email,Password) )
		con.commit()
		msg = "Inserted"
	except:
		con.rollback()
		msg = "Error"

   if request.form.get('login',None)!=None:
	email = request.form['email']
	password = request.form['password']

	cur.execute("SELECT COUNT(*) FROM users where email = ? and password = ?",(email,password))
	count = cur.fetchone()

	if(count[0]==1):
		cur.execute("SELECT * FROM users where email = ? and password = ?",(email,password))
		row = cur.fetchone()
		session['id'] = row[0]
		session['email'] = row[1]
		msg = "Login Success"
	else:
		msg = "Login Fail"
   con.close()
   return redirect(url_for('home',msg=msg))

@app.route('/add_thread/<userid>', methods=['GET', 'POST'])
def add_thread(userid):
   
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   nama = request.form['postName']
   post = request.form['postPost']
   cur = con.cursor()
   cur.execute("SELECT MAX(threadID)+1 FROM thread")
   row = cur.fetchone()
   cur.execute("INSERT INTO thread (threadID, nama, post, userID) values (?,?,?,?)",
   (row[0],nama,post,userid))
   con.commit()
   msg = "Thread successfully added"
   con.close()
   return redirect(url_for('home',msg=msg))

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('id', None)
    return redirect(url_for('home'))

@app.route('/post/<id>')
def post(id):
   
   con = sql.connect('database.db')
   con.row_factory = sql.Row

   cur=con.cursor()
   cur.execute("SELECT * FROM thread WHERE threadId = ?",(id))
   row = cur.fetchone()

   con.close()
   return render_template('post.html',row=row)

@app.route('/comment')
def comment():
   con = sql.connect("database.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("SELECT * FROM users JOIN comment on users.userId = comment.userId")
   rows = cur.fetchall()
   con.close()
   return render_template('comment.html',rows=rows)

@app.route('/post/<userid>', methods=['GET', 'POST'])
def add_comment(userid):

   con = sql.connect("database.db")
   con.row_factory = sql.Row
   nama = request.form['comment']
   cur = con.cursor()
   cur.execute("SELECT MAX(commentID)+1 FROM comment")
   row = cur.fetchone()
   thread = 1
   cur.execute("INSERT INTO comment (commentId, comm, userId) values (?,?,?)",
   (row[0],nama,userid))
   con.commit()
   msg = "Thread successfully added"
   con.close()
   return redirect(url_for('comment'))

@app.route('/delete/<threadId>')
def delete(threadId):
   
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()

   cur.execute("DELETE FROM thread where threadId= ?", (threadId))
   con.commit()
   con.close()
   return redirect(url_for('home'))

@app.route('/deletecomm/<commentId>')
def deletecomm(commentId):
   
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()

   cur.execute("DELETE FROM comment where commentId= ?", (commentId))
   con.commit()
   con.close()
   return redirect(url_for('comment'))


if __name__ == '__main__':
   app.debug= True
   app.run('0.0.0.0',5120)

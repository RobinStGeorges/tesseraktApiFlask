from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import yaml 

app = Flask(__name__)

#	Config
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/')
def index():
	return '<h1>bienvenue sur l\'api de Tesserakt python flask</h1>';
	
#	cours
@app.route('/getAllCours')
def getAllCours():
	cur = mysql.connection.cursor()
	coursCur = cur.execute('select * from cours')
	if coursCur > 0:
		lesCours = cur.fetchall()
		return jsonify(lesCours)
		#return render_template('cours.html',cours = lesCours)


#	Exercice
	
if __name__ == '__main__':
      app.run(debug = true, host='0.0.0.0', port=8081)
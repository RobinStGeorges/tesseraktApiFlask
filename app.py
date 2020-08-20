from flask import Flask, redirect, jsonify
from flask_mysqldb import MySQL
import yaml
import logging

app = Flask(__name__)

#   Config
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)


@app.route('/')
def index():
    return '<h1>bienvenue sur l\'api de Tesserakt python flask</h1>';


##################################################
#   cours
##################################################


@app.route('/cours')
def getAllCours():
    cur = mysql.connection.cursor()
    coursCur = cur.execute('select * from cours')
    if coursCur > 0:
        lesCours = cur.fetchall()
        cur.close()
        return jsonify(lesCours)
    cur.close()


@app.route('/getCours/<id>')
def getCoursById(id):
    cur = mysql.connection.cursor()
    coursCur = cur.execute('select * from cours where id_cours = ' + id)
    if coursCur > 0:
        coursById = cur.fetchall()
        cur.close()
        return jsonify(coursById)
    cur.close()


##################################################
#   Exercice
##################################################

@app.route('/exercices')
def getAllExercices():
    cur = mysql.connection.cursor()
    exercicesCur = cur.execute('select * from exercices')
    if exercicesCur > 0:
        exercices = cur.fetchall()
        cur.close()
        return jsonify(exercices)
    cur.close()


@app.route('/getExercice/<id>')
def getExerciceById(id):
    cur = mysql.connection.cursor()
    exerciceCur = cur.execute('select * from exercices where id_exercice = ' + id)
    if exerciceCur > 0:
        exercice = cur.fetchall()
        cur.close()
        return jsonify(exercice)
    cur.close()


@app.route('/setIsStarted/<id>/<email>')
def setIsStartedById(id, email):
    mysql.connection.autocommit(on=True)
    cur = mysql.connection.cursor()
    email = email.replace('%40', '@')
    email = email.replace('%point', '.')

    # check if line already exist

    curCheck = mysql.connection.cursor()
    responseCheck = curCheck.execute('select * from userdata where id_exercice = ' + id + ' and email like "' + email + '"')
    curCheck.close()
    if responseCheck > 0:
        return jsonify(1)
    else:
        curResultCreate = cur.execute(
            'insert into userdata (id_exercice, email, is_started) values (' + id + ', "' + email + '", true)'
        )
        if curResultCreate > 0:
            cur.close()
            return jsonify(1)
        cur.close()
        app.logger.info(email)
    return jsonify(0)

@app.route('/setIsFinished/<id>/<email>')
def setIsFinishedById(id, email):
    mysql.connection.autocommit(on=True)
    cur = mysql.connection.cursor()
    email = email.replace('%40', '@')
    email = email.replace('%point', '.')
    curResult = cur.execute('update userdata set is_finished = true, date_start = CURRENT_TIMESTAMP where id_exercice = ' + id + ' and email like "' + email + '"')
    if curResult > 0:
        cur.close()
        return jsonify(1)
    cur.close()
    app.logger.info(email)
    return jsonify(0)


##################################################
#   Reponse
##################################################

if __name__ == '__main__':
    app.run(debug=True)

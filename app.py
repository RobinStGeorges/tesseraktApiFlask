from flask import Flask, redirect, jsonify
from flask_mysqldb import MySQL
import yaml
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

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
@cross_origin(supports_credentials=True)
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

@app.route('/getUserResponse')
def getUserResponse():
    cur = mysql.connection.cursor()
    responseCur = cur.execute('select * from userresponse')
    if responseCur > 0:
        responses = cur.fetchall()
        cur.close()
        return jsonify(responses)
    cur.close()
    
@app.route('/checkIsValid/<id>/<email>')
def checkIsValid():
    cur = mysql.connection.cursor()
    responseCur = cur.execute('select * from userdata where id_exercice = ' + id + ' and email like "' + email +'"')
    if responseCur > 0:
        responses = cur.fetchall()
        cur.close()
        return jsonify(0)
    cur.close()
    return jsonify(1)
    
@app.route('/getCubesValuesAll')
def getCubeValueAll():
    cur = mysql.connection.cursor()
    responseCur = cur.execute('select id_cube, action from idcudetoaction')
    if responseCur > 0:
        responses = cur.fetchall()
        cur.close()
        return jsonify(responses)
    cur.close()
    
@app.route('/setCubesValues/<value>', methods = ['GET', 'POST'])
def setCubesValues(value):
    mysql.connection.autocommit(on=True)
    tabVal = value.split(';;')
    del tabVal[0]
    curResultInsert = ''
    for i in range(0, len(tabVal), 1):
        tabi = tabVal[i]
        cur = mysql.connection.cursor()
        curResultInsert += ' ' + insertCubeToAction(str(i), str(tabi))
    return jsonify(curResultInsert);
    

    
def insertCubeToAction(id, action):
    cur = mysql.connection.cursor()
    returnValue = ' none '
    curResultInsert = cur.execute('insert into idcudetoaction (id_cube, action) values (' + str(id)+', "' + str(action) +'") ON DUPLICATE KEY UPDATE action = "' + str(action) +'"')
    if curResultInsert > 1:
        returnValue = curResultInsert.fetchall()
    cur.close()
    return returnValue
    

##################################################
#   User
##################################################

@app.route('/isAdmin/<email>')
def getIsAdmin(email):
    cur = mysql.connection.cursor()
    userResponse = cur.execute('select * from users where email like "' + email + '"')
    if userResponse > 0:
        user = cur.fetchall()
        cur.close()
        if user[0][6]:
            return jsonify(1)
        else:
            return jsonify(0)
    cur.close()
    return jsonify(0)

@app.route('/delete/<mail>')
def deleteUserByMail(mail):
    mail = mail.replace('%40', '@')
    mail = mail.replace('%point', '.')
    mysql.connection.autocommit(on=True)
    cur = mysql.connection.cursor()
    responseCur = cur.execute('DELETE FROM users where email like "' + mail + '"')
    if responseCur > 0:
        return jsonify(1)
    cur.close()
    return jsonify(0)

@app.route('/userdata/<mail>')
def getUserDataByMail(mail):
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select * from userdata where email like "' + mail + '"')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()

if __name__ == '__main__':
    app.run(debug=True)

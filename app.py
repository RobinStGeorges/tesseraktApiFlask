from flask import Flask, redirect, jsonify, request, json
from flask_mysqldb import MySQL
import yaml
import json
from flask_cors import CORS, cross_origin
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import requests

app = Flask(__name__)
CORS(app)

#   Config
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['JWT_SECRET_KEY'] = 'secret'

mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

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
    return 'true';
    

    
def insertCubeToAction(id, action):
    cur = mysql.connection.cursor()
    returnValue = ' none '
    curResultInsert = cur.execute('insert into idcudetoaction (id_cube, action) values (' + str(id)+', "' + str(action) +'") ON DUPLICATE KEY UPDATE action = "' + str(action) +'"')
    if curResultInsert > 0:
        returnValue = cur.fetchall()
        return 'oui'
    cur.close()
    return 'non'
    

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

@app.route('/getUserDataByMail/<email>', methods = ['GET', 'POST'])
def getUserDataByMail(email):
    #args = request.args
    #mail = args['mail']
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select * from userdata where email like "' + email + '"')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()

@app.route('/getUserDataStarted/<email>')
def getUserDataStartedByMail(email):
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select ud.id_exercice, e.titre from userdata as ud join exercices as e on e.id_exercice = ud.id_exercice where ud.email like "' + email + '" and ud.is_started = 1')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()
    
@app.route('/getUserDataFinished/<email>')
def getUserDataFinished(email):
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select ud.id_exercice, e.titre, ud.date_end from userdata as ud join exercices as e on e.id_exercice = ud.id_exercice where ud.email like "' + email + '" and ud.is_finished = 1')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()
    
@app.route('/getDateDif/<email>')
def getDateDif(email):
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select date_start, date_end, id_exercice from userdata as ud  where ud.email like "' + email + '" and ud.is_started = 1 and ud.is_finished = 1')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()

@app.route('/getCoursNameById/<id>')
def getCoursNameById(id):
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select titre from exercices where id_exercice = '+ id)
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()

@app.route('/getUserByMail/<email>')
def getUserByMail(email):
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select first_name, last_name, created from users where email like "' + email + '"')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()
    
@app.route('/users/login', methods=['POST'])
def login():
    cur = mysql.connection.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    cur.execute("SELECT * FROM users where email = '" + str(email) + "'")
    rv = cur.fetchone()
    if bcrypt.check_password_hash(rv[2], password):
        access_token = create_access_token(
            identity={
                'first_name': rv[4],
                'last_name': rv[5],
                'email': rv[1]
            })
        result = access_token
    else:
        result = jsonify({"error": "Invalid username and password"})

    return result
    
@app.route('/users/register', methods=['POST'])
def register():
    cur = mysql.connection.cursor()
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(
        request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    cur.execute(
        "INSERT INTO users (first_name, last_name, email, password, created) VALUES ('"
        + str(first_name) + "','" + str(last_name) + "','" + str(email) +
        "','" + str(password) + "','" + str(created) + "')")
    mysql.connection.commit()

    result = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    }

    return jsonify({'result': result})
    
@app.route('/getCarCommande')
def getCarCommande():
    cur = mysql.connection.cursor()
    dataCur = cur.execute('select ur.coord_x, ur.coord_y, ai.action from userresponse as ur join idcudetoaction as icta on ur.id_box = icta.id_cube join actionid as ai on ai.action = icta.action')
    if dataCur > 0:
        data = cur.fetchall()
        cur.close()
        return jsonify(data)
    cur.close()
    
@app.route('/downloadCours', methods=["GET", "POST"])
def downloadCours():
    #response = requests.get('https://jsonplaceholder.typicode.com/users')
    response = requests.get('http://kireta.pythonanywhere.com/getCoursData')
    data = response.json()

    ress="truncate table cours;"

    col = ""
    val = ""
    isString = ["titre", "description", "contenue", "mediaPath"]
    for item in data:
        col = ""
        val += "("
        for value in item:
            col += " " + str(value) + ","
            # check if field is string field, add " "
            if str(value) in isString:
                val += "\"" + str(item[value]) + "\","
            else:
                val += " " + str(item[value]) + ","
        val = val[:-1]
        val += "),<br>"
    val = val[:-1]
    ress += "insert into cours (" + col + ") values " + val + ";"
    cur = mysql.connection.cursor()
    dataCur = cur.execute(ress)
    
    return dataCur
    
@app.route('/downloadExercice', methods=["GET", "POST"])
def downloadExercice():
    response = requests.get('http://kireta.pythonanywhere.com/getExerciceData')
    data = response.json()

    ress="truncate table cours;"

    col = ""
    val = ""
    isString = ["titre", "description", "contenue", "mediaPath", "imgPath", "imgReponsePath", "cube_needed", "has_finished", "coord_finish"]
    for item in data:
        col = ""
        val += "("
        for value in item:
            col += " " + str(value) + ","
            # check if field is string field, add " "
            if str(value) in isString:
                val += "\"" + str(item[value]) + "\","
            else:
                val += " " + str(item[value]) + ","
        val = val[:-1]
        val += "),<br>"
    val = val[:-1]
    ress += "insert into cours (" + col + ") values " + val + ";"
    return ress
    

app.run(debug=True, port=80, host='0.0.0.0')

from flask import Flask, render_template, request, session, jsonify, make_response, Blueprint
import jwt
from datetime import datetime, timedelta
from functools import wraps
#from routes.auth import routes_auth
#from routes.prueba import vehiculos 
from dotenv import load_dotenv
from function_jwt import write_token, validate_token
from flask_mysqldb import MySQL #configuracion de la base de datos
from werkzeug.security import generate_password_hash, check_password_hash
#import function_jwt

app = Flask(__name__)
#app.register_blueprint(vehiculos, url_prefix='/api')

app.config['SECRET_KEY'] = 'a35db310781d491a841407ae2cb36f50'
app.config['MYSQL_HOST'] = 'us-cdbr-east-06.cleardb.net'#configuracion de la base de datos host
app.config['MYSQL_USER'] = 'bbd292aa23aeaf'#configuracion de la base de datos usuario
app.config['MYSQL_PASSWORD'] = 'ece55924'#configuracion de la base de datos contraseña
app.config['MySQL_DB'] = 'heroku_978ea61906c2949'#configuracion de la base de datos

mysql = MySQL(app)  #se usa para mostrar los datos de la tabla vehiculo

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            Playload = jwt.decode(session['token'], app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'})
    return decorated
@app.route('/hola')
@token_required
def hola():
    return jsonify({'message': 'hola'})
  
#validar inicio de seccion con la base de datos conectada
def validar_usuario(correo, Contraseña):
    try:#el try es para que si hay un error no se caiga el programa
        
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        url = "select Contraseña from heroku_978ea61906c2949.usuario where Correo = '{}'".format(correo)
        print(url)
        cursor.execute(url)#se usa para mostrar los datos de la tabla usuario
        datos = cursor.fetchall()#el fetchall es para que se muestren todos los datos de la consulta
        clave = datos[0][0]
        if len(datos) > 0:#se crea un ciclo for para que se muestren todos los datos de la consulta
            print(clave)
            
            print(Contraseña)
            
            return check_password_hash(clave,Contraseña)
        else:
            print("No existe el usuario")
    except Exception as e:#el except es para que si hay un error no se caiga el programa
        return jsonify({'message': 'error'})
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        correo = data['username']
        contraseña = data['password']
        cursor = mysql.connection.cursor()#se usa para conectar con la base de datos
        if validar_usuario(correo,contraseña) == True:
            return jsonify({'token': write_token(data=request.get_json())})  
        else:
            response = jsonify({"message": "Invalid username or password"})
            response.status_code = 404
            return response

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port="4000", host="0.0.0.0")
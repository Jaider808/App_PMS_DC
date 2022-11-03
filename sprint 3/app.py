from urllib import response
from flask import Flask, render_template, make_response, jsonify, request
import requests #se usa para hacer peticiones a la api
import urllib.parse #es utilizado para codificar los datos
from sympy import arg, hn1#configuracion de la base de datos
#from aiohttp import ClientSession
import asyncio
#from symbol import parameters

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1 style='color:blue' >hola mundo, este es el home.</h1>"

@app.route('/template')
def template():
    return render_template('index.html')
@app.route('/favicon.ico')
def home2():
    return "<h1 style='color:blue' >hola mundo 2, este es el home.</h1>"
@app.route('/api/api-inventario-gv', methods=['GET'])#metodo get de la api inventario
async def api_inventario():
    url = 'https://api-inventario-gv.herokuapp.com/stock'
    data = requests.get(url)
    inventario=[]
    if data.status_code == 200:
        data = data.json()
        if data is not None:
            for e in data['vehiculos']:
                dato = {'Cantidad': e['Cantidad'], 'Caracteristica': e['Caracteristica'], 'Id_vehiculo': e['Id_vehiculo'],
                        'Modelo': e['Modelo'], 'Nombre': e['Nombre'],
                        'Precio': e['Precio'] , 'Tipo': e['Tipo']}#se crea un diccionario para que se muestren los datos de los vehiculos
                inventario.append(dato)#se agrega los datos de los vehiculos a la lista
            return jsonify({'vehiculos': inventario})
        
@app.route('/api/api-signup-gv', methods=['GET'])
def api_signup():#api para iniciar seccion 
        task = []
        url = 'https://api-signup-gv.herokuapp.com/signup'
        data = requests.get(url)
        inventario = []
        if data.status_code == 200:
            data = data.json()
            if data is not None:
                for e in data['personas']:
                    dato = {'Cedula': e['Cedula'], 'Nombre y apellido': e['Nombre y apellido']}#se crea un diccionario para que se muestren los datos de los vehiculos
                    task.append(dato)#se agrega los datos de los vehiculos a la lista
                return jsonify({'personas': task})
@app.route('/api/api-inventario-gv', methods=['GETS','POST'])
async def api_registro():#se crea una funcion para registrar los datos de los vehiculos    
    if request.method == 'POST':#se verifica si el metodo es post
        Cantidad = request.json['Cantidad']#se obtiene el dato de la cantidad
        Caracteristica = request.json['Caracteristica']#se obtiene el dato de la caracteristica
        Modelo = request.json['Modelo']#se obtiene el dato del modelo
        Nombre = request.json['Nombre']#se obtiene el dato del nombre
        Precio = request.json['Precio']#se obtiene el dato del precio
        Tipo = request.json['Tipo']#se obtiene el dato del tipo
    params = {'Cantidad': int(Cantidad), 'Caracteristica': Caracteristica, 'Modelo': Modelo, 'Nombre': Nombre,
                  'Precio': float(Precio), 'Tipo': Tipo}
    response = requests.post('https://api-inventario-gv.herokuapp.com/stock',json=params)
    if response.status_code == 200:
        return jsonify({'message': 'vehiculo añadido'})
    return jsonify({'message': 'vehiculo no añadido'})
#actualizar vehiculo con el id enviadolo a la api-inventario-gv
@app.route('/api/api-inventario-gv/<codigo>', methods=['GETS','PUT'])#se envia el id del vehiculo a actualizar
def api_actualizar(codigo):    #se recibe el id del vehiculo a actualizar
    if request.method == 'PUT':#se verifica que el metodo sea PUT
        Cantidad = request.json['Cantidad']#se recibe la cantidad del vehiculo a actualizar
        Caracteristica = request.json['Caracteristica']#se recibe la caracteristica del vehiculo a actualizar
        Modelo = request.json['Modelo']#se recibe el modelo del vehiculo a actualizar
        Nombre = request.json['Nombre']#se recibe el nombre del vehiculo a actualizar
        Precio = request.json['Precio']#se recibe el precio del vehiculo a actualizar
        Tipo = request.json['Tipo']#se recibe el tipo del vehiculo a actualizar
    params = {'Cantidad': int(Cantidad), 'Caracteristica': Caracteristica, 'Modelo': Modelo, 'Nombre': Nombre,
                  'Precio': float(Precio), 'Tipo': Tipo}#se crea un diccionario con los datos del vehiculo a actualizar
    url_1= 'https://api-inventario-gv.herokuapp.com/stock/'+codigo#se crea la url para enviar el id del vehiculo a actualizar
    response = requests.put(url_1,json=params)#se envia el id del vehiculo a actualizar y los datos a actualizar
    if response.status_code == 200:#se verifica que la peticion se haya realizado correctamente
        return jsonify({'message': 'vehiculo actualizado'})#se retorna un mensaje de que el vehiculo se actualizo
    return jsonify({'message': 'vehiculo no actualizado'})#se retorna un mensaje de que el vehiculo no se actualizo

@app.route('/api/api-inventario-gv/<codigo>', methods=['GETS','DELETE'])#se envia el id del vehiculo a eliminar
def api_eliminar_vehiculo(codigo):
    if request.method == 'DELETE':#se verifica que el metodo sea PUT
        url_1= 'https://api-inventario-gv.herokuapp.com/stock/'+codigo#se crea la url para enviar el id del vehiculo a actualizar
        response = requests.delete(url_1)#se envia el id del vehiculo a actualizar y los datos a actualizar
    if response.status_code == 200:#se verifica que la peticion se haya realizado correctamente
        return jsonify({'message': 'vehiculo eliminado con exito del inventario'})#se retorna un mensaje de que el vehiculo se actualizo
    return jsonify({'message': 'vehiculo no fue elimindao del inventario'})#se retorna un mensaje de que el vehiculo no se actualizo
@app.route('/api/api-signup-gv', methods=['GETS','POST'])#se crea una ruta para registrar un usuario
def api_registro_signup_gv():#se crea una funcion para registrar un usuario
    if request.method == 'POST':#se verifica que el metodo sea POST
        Apellido = request.json['Apellido']#se recibe el apellido del usuario a registrar
        Cedula = request.json['Cedula']#se recibe la cedula del usuario a registrar
        Ciudad = request.json['Ciudad']#se recibe la ciudad del usuario a registrar
        Direccion = request.json['Direccion']#se recibe la direccion del usuario a registrar
        Nombre = request.json['Nombre']#se recibe el nombre del usuario a registrar
        Pais = request.json['Pais']#se recibe el pais del usuario a registrar
        Contraseña = request.json['Contraseña']#se recibe la contraseña del usuario a registrar
    params = {'Apellido': Apellido, 'Cedula': Cedula, 'Ciudad': Ciudad,
                  'Direccion': Direccion, 'Nombre': Nombre, 'Pais': Pais, 'Contraseña': Contraseña}#se crea un diccionario con los datos del usuario a registrar
    response = requests.post('https://api-signup-gv.herokuapp.com/signup',json=params)#se envia los datos del usuario a registrar a la api-signup-gv
    if response.status_code == 200:#se verifica que la peticion se haya realizado correctamente
        return jsonify({'message': 'persona añadida'})#se retorna un mensaje de que el usuario se registro
    return jsonify({'message': 'persona no añadida'})#se retorna un mensaje de que el usuario no se registro
@app.route('/api/api-carrito-compras-gv')#se envia el id del usuario a actualizar
def api_carrito_compras_1():#se crea una funcion para visualizar un carrito de compras
    url = 'https://api-carrito-compras-gv.herokuapp.com/stock'
    data = requests.get(url)
    inventario = []
    if data.status_code == 200:
        data = data.json()
        if data is not None:
            for e in data['vehiculos']:
                dato = {'Cantidad': e['Cantidad'], 'Caracteristica': e['Caracteristica'],
                        'Modelo': e['Modelo'], 'Nombre': e['Nombre'],
                        'Precio': e['Precio'] , 'Tipo': e['Tipo']}#se crea un diccionario para que se muestren los datos de los vehiculos
                inventario.append(dato)#se agrega los datos de los vehiculos a la lista
            return jsonify({'vehiculos': inventario}) 

if __name__== "__main__" :
    app.run(debug=True, port=5000, host='0.0.0.0')
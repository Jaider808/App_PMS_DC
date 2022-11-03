from flask import Blueprint, jsonify, request #importamos el blueprint para poder crear rutas
import requests #importamos requests para poder hacer peticiones a la api
from function_jwt import validate_token #importamos la funcion para validar el token
vehiculos = Blueprint('vehiculos', __name__)

@vehiculos.before_request #antes de que se ejecute la ruta se ejecuta la funcion validate_token 
def verify_token_middleeare(): #creamos la funcion para validar el token
    token = request.headers['Authorization'].split(' ')[1] #obtenemos el token del header
    return validate_token(token) #retornamos la funcion validate_token

@vehiculos.route('/vehiculos/ver', methods=['GET'])
def ver_vehiculos():
    url = 'https://api-inventario-gv.herokuapp.com/stock'
    data = requests.get(url)
    inventario=[]
    if data.status_code == 200:
        data = data.json()
        if data is not None:
            for e in data['vehiculos']:
                dato = { 'Caracteristica': e['Caracteristica'], 'Id_vehiculo': e['Id_vehiculo'],
                        'Modelo': e['Modelo'], 'Nombre': e['Nombre'],
                        'Precio': e['Precio'] , 'Tipo': e['Tipo']}#se crea un diccionario para que se muestren los datos de los vehiculos
                inventario.append(dato)#se agrega los datos de los vehiculos a la lista
            return jsonify({'vehiculos': inventario})  

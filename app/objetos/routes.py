from flask import *
from flask_jwt_extended import  *
# rblueprnt para simplificar las rutas
dispositivosBP = Blueprint("dispositivos",__name__)
# ruta del archivo simplemente usando click y copy paht sobre el archivo destino y origen
RUTA = r"files\devices.json"

#   coje automaticamente la siguente id
def find_next_id():
    objetos = leerFichero()
    if not objetos:
        return 1
    return max(objeto["id"] for objeto in objetos) + 1


#   lee el fichero
def leerFichero():
    try:
        with open(RUTA, "r") as archivo:
            objetos = json.load(archivo)
    except FileNotFoundError:
        objetos = []  # Si no existe el archivo, devuelve una lista vacía
    return objetos

#   escribe el fichero 
def escribirFichero(objetos):
    with open(RUTA, "w") as archivo:
        json.dump(objetos, archivo, indent=4)



#  devuleve todos los dispositivos
#  http://localhost:5050/dispositivos
@dispositivosBP.get('/')
@jwt_required()
def get_objetos():
    objetos= leerFichero()
    return jsonify(objetos)




#   coje un dispositivo
#   http://localhost:5050/dispositivos/2
@dispositivosBP.get('/<int:id>')
@jwt_required()
def get_objeto_id(id):
    objetos= leerFichero()
    for objeto in objetos:
        if objeto['id'] == id:
            return  objeto,200
        
    return { "Error " : "Objeto no encotrado :( " } ,404

#  metodo post que crea un nuevo disopsitivo comprobando que los campos son validos
#  http://localhost:5050/dispositivos
@dispositivosBP.post('/')
@jwt_required()
def add_objeto():
    objetos = leerFichero()
    if request.is_json:
        objeto = request.get_json()
        objeto["id"] = find_next_id()
        if (objeto['tipo'] == "Luz" and objeto['estado'] == "Encendido"  or objeto['estado'] == "Apagado") or (objeto['tipo'] == "Termostato" and objeto['estado'] > 0):
                objetos.append(objeto)
                escribirFichero(objetos)
                return objeto , 201
        return { "Error " : "tipo no valido :( " }

    return { "Error " : "Objeto no es JSON :( " } ,415


#   modifica un dispositivo comprobando que el json por parametro sea del mismo tipo e id 
# http://localhost:5050/dispositivos/2
@dispositivosBP.put('/<int:id>')
@dispositivosBP.patch('/<int:id>')
@jwt_required()
def mofify_objeto_id(id):
    objetos = leerFichero()
    if request.is_json:
        newObjeto = request.get_json()
        for objeto in objetos:
            if objeto['id'] == id:
                if (objeto['tipo'] == "Luz" and objeto['estado'] == "Encendido"  or objeto['estado'] == "Apagado") or (objeto['tipo'] == "Termostato" and objeto['estado'] > 0):
                    if objeto['id']== newObjeto['id'] and objeto['tipo']== newObjeto['tipo']:
                        for atributo in newObjeto:
                            objeto[atributo] = newObjeto[atributo]
                        escribirFichero(objetos)
                        return  objeto,200
                    return { "Error " : "El id o el tipo no coincide :( " } 
                return { "Error " : "Objeto o tipo no valido :( " } 
    return { "Error " : "Objeto no encotrado :( " } ,404

# Ekimina un dispositivo
#  http://localhost:5050/dispositivos/2
@dispositivosBP.delete('/<int:id>')
@jwt_required()
def delete_objeto_id(id):
    objetos= leerFichero()
    for objeto in objetos:
        if objeto['id'] == id:
            objetos.remove(objeto)
            escribirFichero(objetos)
            return  "{}",200
        
    return { "Error " : "Objeto no encotrado :( " } ,404




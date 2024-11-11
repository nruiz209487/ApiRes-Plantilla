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


#    http://localhost:5050
# @app.route('/')
# def index():
#     return("Servicio activo")

#   http://localhost:5050/dispositivos
@dispositivosBP.get('/')
@jwt_required()
def get_objetos():
    objetos= leerFichero()
    return jsonify(objetos)



#   http://localhost:5050/dispositivos/2
@dispositivosBP.get('/<int:id>')
def get_objeto_id(id):
    objetos= leerFichero()
    for objeto in objetos:
        if objeto['id'] == id:
            return  objeto,200
        
    return { "Error " : "Objeto no encotrado :( " } ,404

#   http://localhost:5050/dispositivos
@dispositivosBP.post('/')
def add_objeto():
    objetos = leerFichero()
    if request.is_json:
        objeto = request.get_json()
        objeto["id"] = find_next_id()
        objetos.append(objeto)
        escribirFichero(objetos)
        return objeto , 201

    return { "Error " : "Objeto no es JSON :( " } ,415


#   http://localhost:5050/dispositivos/2
@dispositivosBP.put('/<int:id>')
@dispositivosBP.patch('/<int:id>')
def mofify_objeto_id(id):
    objetos = leerFichero()
    if request.is_json:
        newObjeto = request.get_json()
        for objeto in objetos:
            if objeto['id'] == id:
                for atributo in newObjeto:
                    objeto[atributo] = newObjeto[atributo]
                escribirFichero(objetos)
                return  objeto,200
            
    return { "Error " : "Objeto no encotrado :( " } ,404

#   http://localhost:5050/dispositivos/2
@dispositivosBP.delete('/<int:id>')
def delete_objeto_id(id):
    objetos= leerFichero()
    for objeto in objetos:
        if objeto['id'] == id:
            objetos.remove(objeto)
            escribirFichero(objetos)
            return  "{}",200
        
    return { "Error " : "Objeto no encotrado :( " } ,404




from flask import Blueprint, request, jsonify
import json
#  Blue print que simplifica las rutas 
subobjetosBP = Blueprint("subobjetos", __name__)
# ruta del archivo simplemente usando click y copy paht sobre el archivo destino y origen
RUTA = r"files\subobjetos.json"

#   coje automaticamente la siguente id
def find_next_id():
    subobjetos = leerFichero()
    if not subobjetos:
        return 1
    return max(subobjeto["id"] for subobjeto in subobjetos) + 1

#   lee el fichero
def leerFichero():
    try:
        with open(RUTA, "r") as archivo:
            subobjetos = json.load(archivo)
    except FileNotFoundError:
        subobjetos = []  # Si no existe el archivo, devuelve una lista vacía
    return subobjetos

#   escribe el fichero 
def escribirFichero(subobjetos):
    with open(RUTA, "w") as archivo:
        json.dump(subobjetos, archivo, indent=4)


#   http://localhost:5050/objetos/1/subobjetos
@subobjetosBP.get('/')
def get_subobjetos_por_objeto(obj_id):
    subobjetos = leerFichero()
    result = [subobjeto for subobjeto in subobjetos if subobjeto['idObjeto'] == obj_id]
    if result:
        return jsonify(result), 200
    return { "Error": "No subobjetos found for this object" }, 404

#   http://localhost:5050/objetos/1/subobjetos/1
@subobjetosBP.get('/<int:sub_id>')
def get_subobjeto_por_id(obj_id, sub_id):
    subobjetos = leerFichero()
    for subobjeto in subobjetos:
        if subobjeto['idObjeto'] == obj_id and subobjeto['id'] == sub_id:
            return jsonify(subobjeto), 200
    return { "Error": "Subobjeto no encontrado" }, 404

#   http://localhost:5050/objetos/1/subobjetos
@subobjetosBP.post('')
def add_subobjeto(obj_id):
    subobjetos = leerFichero()
    if request.is_json:
        subobjeto = request.get_json()
        subobjeto["id"] = find_next_id()
        subobjeto["idObjeto"] = obj_id  # Asociamos el subobjeto con el objeto por su id
        subobjetos.append(subobjeto)
        escribirFichero(subobjetos)
        return jsonify(subobjeto), 201

    return { "Error": "Subobjeto debe ser un JSON" }, 415

#   http://localhost:5050/objetos/1/subobjeto/1
@subobjetosBP.put('/<int:sub_id>')
@subobjetosBP.patch('/<int:sub_id>')
def modify_subobjeto(obj_id, sub_id):
    subobjetos = leerFichero()
    if request.is_json:
        newSubobjeto = request.get_json()
        for subobjeto in subobjetos:
            if subobjeto['idObjeto'] == obj_id and subobjeto['id'] == sub_id:
                for key, value in newSubobjeto.items():
                    subobjeto[key] = value
                escribirFichero(subobjetos)
                return jsonify(subobjeto), 200
    return { "Error": "Subobjeto no encontrado" }, 404

#   http://localhost:5050/objetos/1/subobjeto/1
@subobjetosBP.delete('/<int:sub_id>')
def delete_subobjeto(obj_id, sub_id):
    subobjetos = leerFichero()
    for subobjeto in subobjetos:
        if subobjeto['idObjeto'] == obj_id and subobjeto['id'] == sub_id:
            subobjetos.remove(subobjeto)
            escribirFichero(subobjetos)
            return {}, 200
    return { "Error": "Subobjeto no encontrado" }, 404

from flask import Blueprint, request, jsonify
import json
import bcrypt
from flask_jwt_extended import create_access_token

# rblueprnt para simplificar las rutas
usuariosBP = Blueprint("usuarios", __name__)
# ruta del archivo simplemente usando click y copy paht sobre el archivo destino y origen
RUTA = r"files\usuarios.json"

# LEE EL FICHERO DE DESTINO 
def leerFichero():
    try:
        with open(RUTA, "r") as archivo:
            subobjetos = json.load(archivo)
    except FileNotFoundError:
        subobjetos = []  # Si no existe el archivo, devuelve una lista vacía
    return subobjetos
# ESCRIBE EN  EL FICHERO DE DESTINO 
def escribirFichero(subobjetos):
    with open(RUTA, "w") as archivo:
        json.dump(subobjetos, archivo, indent=4)

#  http://localhost:5050/usuarios/registrar  
# metodo registar que registra un nuevo usuario JSON
  # {
  #    "nombre": "examen",
  #    "contrasenya": "123"
  # }
    
@usuariosBP.post("/registrar")
def registrarUsuario():
    usuarios = leerFichero()
    if request.is_json:
        usuario = request.get_json()
        contrasenya =usuario["contrasenya"].encode("utf-8")
        sal = bcrypt.gensalt()
        hashContrasenya = bcrypt.hashpw(contrasenya,sal).hex()
        usuario["contrasenya"] = hashContrasenya
        usuarios.append(usuario)
        escribirFichero(usuarios)
        token = create_access_token(identity=usuario["nombre"])
        return{"token": token },201
    return{"error": "Request must be JSON"} ,415

  # {
  #    "nombre": "examen",
  #    "contrasenya": "123"
  # }
# metodo loginUsuario que  DEVULEVE UN TOKEN DE ACCESO
#  http://localhost:5050/usuarios/login
@usuariosBP.get("/login")
def loginUsuario():
    usuarios = leerFichero()
    if request.is_json:
        usuario = request.get_json()
        nombre = usuario["nombre"]
        contrasenya =usuario["contrasenya"].encode("utf-8")
        for usuariosEnArchivo in usuarios:
            if usuariosEnArchivo["nombre"] == nombre:
                contrasenyaEnArchivo = usuariosEnArchivo["contrasenya"]
                if bcrypt.checkpw(contrasenya,bytes.fromhex(contrasenyaEnArchivo)):
                    token = create_access_token(identity=usuario["nombre"])
                    return{"token": token },200
                else:
                    return{"error": "contrasenya o usuario erroneo" },401
        return{"error": "usuario no encontrado" },404
    return{"error": "no es json" },404
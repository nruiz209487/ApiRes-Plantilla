from flask import * 
from flask_jwt_extended import  *
from.objetos.routes import objetosBP
from.subobjetos.routes import subobjetosBP
from.usuarios.routes import usuariosBP

#inicializacion de apps
app = Flask(__name__)
#configuracion para claves 
app.config["SECRET_KEY"] = 'Wl9f8hfnD7kl@Z9vQm1Uj7PQm3Bp4r2Y9H2uP&6fgtXZ9p2pN5'
jwt = JWTManager(app)

#Blue prints de cada objeto para su suo en rutas 
app.register_blueprint(objetosBP,url_prefix="/objetos")
app.register_blueprint(subobjetosBP, url_prefix="/objetos/<int:obj_id>/subobjetos")
app.register_blueprint(usuariosBP, url_prefix="/usuarios")
from flask import Flask, Blueprint, Response
import os
from service.produtoService import produto_service
from service.usuarioService import usuario_service
from service.grupoService import grupo_service

app = Flask(__name__)

app.register_blueprint(produto_service)
app.register_blueprint(usuario_service)
app.register_blueprint(grupo_service)



@app.route('/')
def home():
    return ""
app.run()


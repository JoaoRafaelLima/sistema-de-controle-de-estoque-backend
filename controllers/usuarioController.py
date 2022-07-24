import sqlite3
from exceptions.usuarioException import LoginJaCadastrado
from exceptions.usuarioException import UsuarioInexistente
from repository.usuarioRepository import UsuarioRepository
from models.usuarioModel import UsuarioModel
from hashlib import sha256
import json
import jwt
import datetime
import os

class UsuarioController:

    def __init__(self):
        self.usuarioRepository = UsuarioRepository()

    def listarUsuarios(self):
        usuarios = []
        try:
            resultado = self.usuarioRepository.listarUsuarios()
            for item in resultado:
                usuario = UsuarioModel(item[1], item[2], item[3], item[0] )
                usuarios.append(usuario.base_data())
            return (json.dumps(usuarios), 200)
        except sqlite3.OperationalError:
            return (json.dumps({"Erro":"Erro na operação, tente novamente dentro de alguns minutos"}), 500)

    def inserirUsuario(self, data):
        
        try:
            senha = sha256(data["senha"].encode())
            usuario = UsuarioModel(data["nome"], data["login"], senha.hexdigest())
            self.usuarioRepository.inserirUsuario(usuario)
            return (json.dumps({"Message": "Usuario inserido com sucesso"}), 201)
        except TypeError as e:
            print(e)
            return (json.dumps({"Message":"Dados invalidos"}), 400)
        except LoginJaCadastrado:
            return (json.dumps({"Error": "O login já existe"}), 400)
    
    def atualizarUsuario(self, data):
        try:
            senha = sha256(data["senha"].encode())
            usuario = UsuarioModel(data["nome"], data["login"], senha.hexdigest(), data["id"])
            self.usuarioRepository.atualizarUsuario(usuario)
            return (json.dumps({"Message": "Usuario atualizado com sucesso"}), 200)
        except UsuarioInexistente:
            return (json.dumps({"Error": "Usuario inexistente"}), 400)
        
        except LoginJaCadastrado:
            return (json.dumps({"Error": "O login já existe"}), 400)

    def deletarUsuario(self, usuario_id) -> tuple: 
        try:
            self.usuarioRepository.deletarUsuario(usuario_id)
            return (json.dumps({"Message": "Usuario excluido com sucesso"}), 200)
        except UsuarioInexistente:
            return (json.dumps({"Error": "Usuario inexistente"}), 400)
        
    def login(self, data):
        try:
            resultado = self.usuarioRepository.buscarUsuarioPorLogin(data["login"])
            usuario = resultado
            if usuario[3] == sha256(data["senha"].encode()).hexdigest():
                payload = {
                    "id": usuario[0],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
                }
                token = jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")
                return (json.dumps({"Token": token}), 200)
            else:
                return (json.dumps({"Erro": "Senha incorreta"}), 400)
        except UsuarioInexistente as e:
            return (json.dumps({"Error": "error"}), 400)
        except sqlite3.OperationalError:
            return (json.dumps({"Erro":"Erro na operação, tente novamente dentro de alguns minutos"}), 500)
        


        
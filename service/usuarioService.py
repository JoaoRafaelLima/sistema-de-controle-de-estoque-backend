from controllers.usuarioController import UsuarioController
from flask import Blueprint, request, make_response
from service.authenticate import login_required

usuario_service = Blueprint("usuario_service", __name__)
usuarioController = UsuarioController()

@usuario_service.route("/usuarios", methods=['GET'])
@login_required
def listarUsuarios(args):
    response, status = usuarioController.listarUsuarios()
    return make_response(response, status)

@usuario_service.route("/novo-usuario", methods=['POST'])
@login_required
def inserirUsuario(args):
    response, status = usuarioController.inserirUsuario(request.json)
    return make_response(response, status)

@usuario_service.route("/atualizar-usuario", methods=['PUT'])
@login_required
def atualizarUsuario(args):
    response, status = usuarioController.atualizarUsuario(request.json)
    return make_response(response, status)

@usuario_service.route("/deletar-usuario/<int:id>", methods=['DELETE'])
@login_required
def deletarUsuario(args, id):
    response, status = usuarioController.deletarUsuario(id)
    return make_response(response, status)

# autenticacao
@usuario_service.route("/auth/login", methods=['POST'])
def login():
    response, status = usuarioController.login(request.json)
    return make_response(response, status)
    
    
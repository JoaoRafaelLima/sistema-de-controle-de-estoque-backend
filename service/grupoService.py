from flask import Blueprint, make_response, request
from controllers.grupoController import GrupoController


grupoController = GrupoController()
grupo_service = Blueprint("grupo_service", __name__)

@grupo_service.route("/grupos", methods=["GET"])
def listarGrupos():
    response, status = grupoController.listarGrupos()
    return make_response(response, status)

@grupo_service.route("/novo-grupo", methods=["POST"])
def inserirGrupo():
    response, status = grupoController.inserirGrupo(request.json)
    return make_response(response, status)

@grupo_service.route("/atualizar-grupo", methods=["PUT"])
def atualiarGrupo():
    response, status = grupoController.atualizarGrupo(request.json)
    return make_response(response, status)

@grupo_service.route("/deletar-grupo/<int:id>", methods=["DELETE"])
def deletarGrupo(id):
    response, status = grupoController.deletarGrupo(id)
    return make_response(response, status)

@grupo_service.route("/grupo/<int:id>/produtos")
def listarProdutosPorGrupo(id):
    response, status = grupoController.listarProdutosPorGrupo(id)
    return make_response(response, status)

@grupo_service.route("/grupo/movimentar-produto", methods=["PUT"])
def movimentar():
    response, status = grupoController.movimentarProduto(request.json)
    return  make_response(response, status)

from flask import Blueprint, make_response, request
from controllers.grupoController import GrupoController
from service.authenticate import login_required


grupoController = GrupoController()
grupo_service = Blueprint("grupo_service", __name__)

@grupo_service.route("/grupos", methods=["GET"])
@login_required
def listarGrupos(args):
    response, status = grupoController.listarGrupos()
    return make_response(response, status)

@grupo_service.route("/novo-grupo", methods=["POST"])
@login_required
def inserirGrupo(args):
    response, status = grupoController.inserirGrupo(request.json)
    return make_response(response, status)

@grupo_service.route("/atualizar-grupo", methods=["PUT"])
@login_required
def atualiarGrupo(args):
    response, status = grupoController.atualizarGrupo(request.json)
    return make_response(response, status)

@grupo_service.route("/deletar-grupo/<int:id>", methods=["DELETE"])
@login_required
def deletarGrupo(args, id):
    response, status = grupoController.deletarGrupo(id)
    return make_response(response, status)

@grupo_service.route("/grupo/<int:id>/produtos")
@login_required
def listarProdutosPorGrupo(args, id):
    response, status = grupoController.listarProdutosPorGrupo(id)
    return make_response(response, status)

@grupo_service.route("/grupo/movimentar-produto", methods=["PUT"])
@login_required
def movimentar(args):
    response, status = grupoController.movimentarProduto(request.json)
    return  make_response(response, status)

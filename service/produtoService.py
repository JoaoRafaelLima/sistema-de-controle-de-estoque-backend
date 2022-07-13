from flask import Blueprint, request, make_response
from controllers.produtoController import ProdutoController
from service.authenticate import login_required

produtoController = ProdutoController()

produto_service = Blueprint("produto_service", __name__)

@produto_service.route("/produto/<int:id>", methods=['GET'])
@login_required
def selecionarProduto(args, id):
    response, status = produtoController.selecionarProduto(id)
    return make_response(response, status)

@produto_service.route("/produtos", methods=['GET'])
@login_required
def listarProdutos(args):
    response, status = produtoController.listarProdutos()
    return make_response(response, status)

@produto_service.route("/novo-produto", methods=['POST'])
@login_required
def inserirProduto(args):
    response, status = produtoController.inserirProduto(request.json)
    return make_response(response, status)

@produto_service.route("/atualizar-produto", methods=['PUT'])
@login_required
def atualizarProduto(args):
    response, status = produtoController.atualizarProduto(request.json)
    return make_response(response, status)

@produto_service.route("/deletar-produto/<int:id>", methods=['DELETE'])
@login_required
def deletarProduto(args, id):
    response, status = produtoController.deletarProduto(id)
    return make_response(response, status)

@produto_service.route("/produto/reposicao", methods=["PUT"])
@login_required
def reporProduto(args):
    response, status = produtoController.reporProduto(request.json)
    return  make_response(response, status)
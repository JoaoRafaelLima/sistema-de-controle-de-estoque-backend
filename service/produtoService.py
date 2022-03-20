from urllib import response
from flask import Blueprint, request, make_response
from controllers.produtoController import ProdutoController
import json

produtoController = ProdutoController()

produto_service = Blueprint("produto_service", __name__)

@produto_service.route("/produto/<int:id>", methods=['GET'])
def selecionarProduto(id):
    response, status = produtoController.selecionarProduto(id)
    return make_response(response, status)

@produto_service.route("/produtos", methods=['GET'])
def listarProdutos():
    response, status = produtoController.listarProdutos()
    return make_response(response, status)

@produto_service.route("/novo-produto", methods=['POST'])
def inserirProduto():
    response, status = produtoController.inserirProduto(request.json)
    return make_response(response, status)

@produto_service.route("/atualizar-produto", methods=['PUT'])
def atualizarProduto():
    response, status = produtoController.atualizarProduto(request.json)
    return make_response(response, status)

@produto_service.route("/deletar-produto/<int:id>", methods=['DELETE'])
def deletarProduto(id):
    response, status = produtoController.deletarProduto(id)
    return make_response(response, status)
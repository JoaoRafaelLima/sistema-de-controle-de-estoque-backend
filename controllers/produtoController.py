import sqlite3
from exceptions.produtoExceptions import ProdutoNaoEncontrado
from repository.produtoRepository import ProdutoRepository
from models.produtoModel import ProdutoModel
import json

class ProdutoController:

    def __init__(self):
        self.produtoRepository = ProdutoRepository()


    def selecionarProduto(self, id):
        try:
            resultado = self.produtoRepository.selecionarProduto(id)
            if len(resultado) == 0:
                return {"Error": "produto não encontrado"}
            else:
                data = resultado[0]
                produto = ProdutoModel(data[1], data[2], data[3], data[0] )
                return (json.dumps(produto.__dict__), 200)
        except Exception as e:
            return (json.dumps({"Error": "Error"}), 400)

    def listarProdutos(self):   
        produtos = []
        try:
            resultado = self.produtoRepository.listarProdutos()
            for item in resultado:
                produto = ProdutoModel(item[1], item[2], None, None, item[0] )
                produtos.append(produto.base_data())
            return (json.dumps(produtos), 200)
        except sqlite3.OperationalError:
            return (json.dumps({"Erro":"Erro na operação, tente novamente dentro de alguns minutos"}), 500)
        
    
    def inserirProduto(self, data):
        try:
            print(data)
            produto = ProdutoModel(data["nome"], data["valor"], data["quantidade"], data["grupo"])
            self.produtoRepository.inserirProduto(produto)
            return (json.dumps({"Message": "Produto inserido com sucesso"}), 200)
        except Exception as e:
            return (json.dumps({"Error": f"Falha na operação, {e}"}), 500)
        
        
    def atualizarProduto(self, data):
        try:
            produto = ProdutoModel(data["nome"], data["valor"], None, None, data["id"])
            self.produtoRepository.atualizarProduto(produto)
            return (json.dumps({"Message": "Produto atualizado com sucesso"}), 200)
        except Exception as e:
            return(json.dumps({"Error": f"Falha ao atualizar o produto, {e}"}), 500)
    
    def deletarProduto(self, data):
        try:
            self.produtoRepository.deletarProduto(data)
            return (json.dumps({"Message": "Produto deletado com sucesso"}), 200)
        except ProdutoNaoEncontrado:
            return (json.dumps({"Error": "O produto informado não está cadastrado"}), 500)

        
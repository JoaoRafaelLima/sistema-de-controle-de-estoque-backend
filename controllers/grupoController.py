from repository.grupoRepository import GrupoRepository
from models.grupoModel import GrupoModel
from models.produtoModel import ProdutoModel
from exceptions.grupoExceptions import GrupoInexistente, QuantidadeInsuficenteParaMovimentacao
import json


class GrupoController:

    def __init__(self) -> None:
        self.grupoRepository = GrupoRepository()

    def listarGrupos(self):
        grupos = []
        try:
            resultado = self.grupoRepository.listarGrupos()
            if len(resultado) == 0:
                return (json.dumps({"Error": "Não há grupos cadastrados."}), 400)
            else:
                for item in resultado:
                    grupo = GrupoModel(item[1], item[2], item[0])
                    grupos.append(grupo.__dict__)
                
                return (json.dumps(grupos), 200)
        except Exception as error:
            return (json.dumps({"Error": str(error)}), 400)
    
    def inserirGrupo(self, data):
        try:
            grupo = GrupoModel(data["nome"], data["descricao"])
            self.grupoRepository.inserirGrupo(grupo)
            return (json.dumps({"Message": "Grupo inserido com sucesso!"}), 200)
        except Exception as error:
            return (json.dumps({"Error": str(error)}))
       
    def atualizarGrupo(self, data):
        try:
            grupo = GrupoModel(data["nome"], data["descricao"], data["id"])
            self.grupoRepository.atualizarGrupo(grupo)
            return (json.dumps({"Message": "Grupo atualizado com sucesso!"}), 200)
        except GrupoInexistente as error:
            return (json.dumps({"Error": str(error)}),400)
        except Exception as error:
            return (json.dumps({"Error": str(error)}), 400)

    def deletarGrupo(self, id):
        try:
            self.grupoRepository.deletarGrupo(id)
            return (json.dumps({"Message": "Grupo deletado com sucesso!"}), 200)
        except GrupoInexistente as error:
            return (json.dumps({"Error": str(error)}), 400)

    def listarProdutosPorGrupo(self, id_grupo):
        try:
            result = self.grupoRepository.listarProdutosPorGrupo(id_grupo)
            produtos = []
            for item in result[0]:
                produto = ProdutoModel(item[1], item[2], item[3], result[1], item[0])
                produtos.append(produto.__dict__)

            return (json.dumps({"Grupo": result[2], "Produtos": produtos}), 200)
            
        except GrupoInexistente as error:
            return (json.dumps({"Error": str(error)}), 400)
    
    def movimentarProduto(self, data):
        try:
            self.grupoRepository.movimentar(data["produto_id"], data["grupo1_id"], data["grupo2_id"], data["quantidade"])
            return (json.dumps({"Message": "Movimentação concluida com sucesso!"}), 200)

        except QuantidadeInsuficenteParaMovimentacao as error:
            return (json.dumps({"Error": str(error)}), 400)
        
        except GrupoInexistente as error:
            return (json.dumps({"Error": str(error)}), 400)

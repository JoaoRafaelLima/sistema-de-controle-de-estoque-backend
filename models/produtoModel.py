


class ProdutoModel(object):

    def __init__(self, nome, valor, quantidade, grupo, id=None):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.grupo = grupo
        self.quantidade  = quantidade
    
    def base_data(self):
        return {
            "id": self.id,
            "nome":self.nome,
            "valor": self.valor
        }
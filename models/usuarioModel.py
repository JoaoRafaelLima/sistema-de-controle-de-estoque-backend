


class UsuarioModel:

    def __init__(self, nome, login, senha, id=None):
        self.id = id
        self.nome = nome
        self.login = login
        self.senha = senha
    
    def base_data(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "login": self.login
        }


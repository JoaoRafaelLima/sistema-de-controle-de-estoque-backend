from exceptions.usuarioException import UsuarioInexistente, LoginJaCadastrado
from repository.conexao import conexaoFactory
from models.usuarioModel import UsuarioModel


class UsuarioRepository:

    def __init__(self):
        self.conexao = conexaoFactory()
        self.cursor = self.conexao.cursor()
       
    def listarUsuarios(self):
        query = "SELECT * FROM usuarios"
        self.cursor.execute(query)
        tmp = self.cursor.fetchall()
        return tmp
    
    def inserirUsuario(self, usuario: UsuarioModel):
        self.__verificarUsario("login", usuario.login)
        query = "INSERT INTO usuarios(nome, login, senha) VALUES(?,?,?);"
        self.cursor.execute(query, (usuario.nome, usuario.login, usuario.senha))
        self.conexao.commit()
        return True
    
    def atualizarUsuario(self, usuario: UsuarioModel):
        self.__verificarUsario("id", usuario.id)
        self.__verificarUsario("login", usuario.login)
        query = "UPDATE usuarios SET nome = ?, login = ?, senha = ? WHERE id = ?"
        self.cursor.execute(query, (usuario.nome, usuario.login, usuario.senha, usuario.id))
        self.conexao.commit()
        return True

    def deletarUsuario(self, usuario_id:int):
        self.__verificarUsario("id", usuario_id)
        query = "DELETE FROM usuarios WHERE id = ?"
        self.cursor.execute(query, (usuario_id,))
        self.conexao.commit()
        return True
    
    def buscarUsuarioPorLogin(self, login:str):
        query = "SELECT * FROM usuarios WHERE login = ?"
        self.cursor.execute(query, (login,))
        tmp = self.cursor.fetchone()
        if tmp == None:
            raise UsuarioInexistente()
        return tmp

    def __verificarUsario(self, coluna, valor):
        query = f"SELECT * FROM usuarios WHERE {coluna} = ?"
        self.cursor.execute(query, (valor,))
        if coluna == "login":
            if self.cursor.fetchone() != None:
                raise LoginJaCadastrado()
            return True
        else:
            if self.cursor.fetchone() == None:
                raise UsuarioInexistente()
            return True


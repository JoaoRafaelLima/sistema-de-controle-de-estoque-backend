from exceptions.produtoExceptions import ProdutoNaoEncontrado
from repository.conexao import conexaoFactory
from models.produtoModel import ProdutoModel


class ProdutoRepository:

    def __init__(self):
        self.conexao = conexaoFactory()
        self.cursor = self.conexao.cursor()
    
    def selecionarProduto(self, id):
        query = "SELECT * FROM produtos WHERE id = ?"
        self.cursor.execute(query, (id,))
        tmp = self.cursor.fetchall()
        return tmp

    def listarProdutos(self):
        query = "SELECT * FROM produtos"
        self.cursor.execute(query)
        tmp = self.cursor.fetchall()
        return tmp

    def inserirProduto(self, produto: ProdutoModel):
        query = "INSERT INTO produtos(nome, valor) VALUES(?,?)"
        result = self.cursor.execute(query, (produto.nome, produto.valor))
        print(produto.grupo, result.lastrowid, produto.quantidade)
        query2 = "INSERT INTO grupo_produto(grupo_id, produto_id, quantidade) VALUES(?,?,?);"
        self.cursor.execute(query2, (produto.grupo, result.lastrowid, produto.quantidade))
        self.conexao.commit()
        return True
    
    def atualizarProduto(self, produto: ProdutoModel):
        query = "UPDATE produtos SET nome = ?, valor = ? WHERE id = ?"
        self.cursor.execute(query, (produto.nome, produto.valor, produto.id))
        self.conexao.commit()
        return True

    def deletarProduto(self, id):
        
        query = "SELECT * FROM produtos WHERE id = ?"
        self.cursor.execute(query, (id,))

        if self.cursor.fetchone() == None:
            raise ProdutoNaoEncontrado()

        query2 = "DELETE FROM produtos WHERE id = ?"
        self.cursor.execute(query2, (id,))
        self.conexao.commit()

    
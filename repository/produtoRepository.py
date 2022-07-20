from exceptions.produtoExceptions import ProdutoNaoEncontrado
from exceptions.grupoExceptions import GrupoOuProdutoNaoEncontrado
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
    
    def reporProduto(self, grupo_id, produto_id, quantidade_a_repor):
        #query que verifica se há um registro que relaciona o produto solicitado com o grupo 2
        query = "SELECT * FROM grupo_produto WHERE grupo_id = ? AND produto_id = ?"
        self.cursor.execute(query, (grupo_id, produto_id))
        result = self.cursor.fetchone()
        if result != None:
            quantidade_atual = result[2]
            query2 = "UPDATE grupo_produto SET quantidade = ? WHERE grupo_id = ? and produto_id = ?"
            quantidade_atualizada = quantidade_atual + quantidade_a_repor
            self.cursor.execute(query2, (quantidade_atualizada, grupo_id, produto_id))
            self.conexao.commit()
        else:
            raise GrupoOuProdutoNaoEncontrado()

    
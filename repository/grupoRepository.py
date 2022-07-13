from repository.conexao import conexaoFactory
from models.grupoModel import GrupoModel
from exceptions.grupoExceptions import GrupoInexistente, QuantidadeInsuficenteParaMovimentacao, GrupoOuProdutoNaoEncontrado


class GrupoRepository:

    def __init__(self):
        self.conexao = conexaoFactory()
        self.cursor = self.conexao.cursor()
    
    def selecionarGrupo(self, id):
        query = "SELECT * FROM grupo WHERE id = ?"
        self.cursor.execute(query, (id,))
        tmp = self.cursor.fetchall()
        return tmp
         
    def listarGrupos(self):
        self.cursor.execute("SELECT * FROM grupo")
        tmp = self.cursor.fetchall()
        return tmp

    def inserirGrupo(self, grupo:GrupoModel):
        query = "INSERT INTO grupo(nome, descricao) VALUES(?,?);"
        self.cursor.execute(query, (grupo.nome, grupo.descricao))
        self.conexao.commit()
        return True

    def atualizarGrupo(self, grupo:GrupoModel):

        if not self.selecionarGrupo(grupo.id):
            raise GrupoInexistente()
        query = "UPDATE grupo  SET nome = ?, descricao = ? WHERE id = ?;"
        self.cursor.execute(query, (grupo.nome, grupo.descricao, grupo.id))
        self.conexao.commit()
        return True

    def deletarGrupo(self, id:int):
        if not self.selecionarGrupo(id):
            raise GrupoInexistente()
        query = "DELETE FROM grupo WHERE id = ?;"
        self.cursor.execute(query, (id,))
        self.conexao.commit()
        return True
    
    def listarProdutosPorGrupo(self, grupo_id):
        if not self.selecionarGrupo(grupo_id):
            raise GrupoInexistente()
        query = """
        SELECT produtos.id, produtos.nome, produtos.valor, grupo_produto.quantidade
        FROM produtos INNER JOIN grupo_produto ON produtos.id = grupo_produto.produto_id
        WHERE grupo_produto.grupo_id = ?
        """
        self.cursor.execute(query, (grupo_id,))
        rows = self.cursor.fetchall()
        self.cursor.execute("SELECT grupo.nome FROM grupo WHERE id = ?", (grupo_id,))
        grupo = self.cursor.fetchall()[0]
        return (rows, grupo_id, grupo[0])
    

    def movimentar(self, produto_id, grupo1_id, grupo2_id, quantidade_solicitada):

        if not self.selecionarGrupo(grupo1_id):
            raise GrupoInexistente(grupo1_id)
        if not self.selecionarGrupo(grupo2_id):
            raise GrupoInexistente(grupo2_id)

        # query que busca o quantidade atual do produto no grupo 1
        query1 = """
        SELECT grupo_produto.quantidade FROM  grupo_produto 
        WHERE grupo_produto.grupo_id = ? AND grupo_produto.produto_id = ?"""
        self.cursor.execute(query1, (grupo1_id, produto_id))
        quantidade_atual = self.cursor.fetchone()

        if quantidade_solicitada > quantidade_atual[0]:
            raise QuantidadeInsuficenteParaMovimentacao()
        else:
            #query que atualiza a quantidade do  produto no grupo 1
            quantidade_atualizada_grupo1 = quantidade_atual[0] - quantidade_solicitada
            query2 = "UPDATE grupo_produto SET quantidade = ? WHERE grupo_id = ? AND produto_id = ?"
            self.cursor.execute(query2, (quantidade_atualizada_grupo1, grupo1_id, produto_id))

            #query que verifica se há um registro que relaciona o produto solicitado com o grupo 2
            query3 = "SELECT * FROM grupo_produto WHERE grupo_id = ? AND produto_id = ?"
            self.cursor.execute(query3, (grupo2_id, produto_id))
            if self.cursor.fetchone() == None:
                # caso o produto solicitado ainda não tem uma relação com o grupo que irá receber,  será criado um registro
                
                #query que irá adicionar o registro ao grupo 2
                query4 = "INSERT INTO grupo_produto(grupo_id, produto_id, quantidade) VALUES(?,?,?);"
                self.cursor.execute(query4, (grupo2_id, produto_id, quantidade_solicitada))
            else:
                # caso já tenha um registro, será atualizado 

                #query que vai pegar a quantidade atual do item no grupo 2
                query5 = """
                SELECT grupo_produto.quantidade FROM  grupo_produto 
                WHERE grupo_produto.grupo_id = ? AND grupo_produto.produto_id = ?"""
                self.cursor.execute(query5, (grupo2_id, produto_id))
                quantidade_atual = self.cursor.fetchone()[0]

                #query que vai atualizar a quantidade
                query4 = "UPDATE grupo_produto SET quantidade = ? WHERE grupo_id = ? AND produto_id = ?"
                quantidade_total = quantidade_atual + quantidade_solicitada
                self.cursor.execute(query4, (quantidade_total, grupo2_id,produto_id))
            
            self.conexao.commit()
            return True


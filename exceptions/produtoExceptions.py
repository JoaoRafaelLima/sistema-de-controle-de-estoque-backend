

class ProdutoNaoEncontrado(Exception):
    def __init__(self) -> None:
        super().__init__("Produto não encontrado")

class QuantidadeInsuficiente(Exception):
    def __init__(self) -> None:
        super().__init__("Quantidade insuficiente")
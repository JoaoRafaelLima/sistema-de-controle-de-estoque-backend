

class GrupoInexistente(Exception):
    def __init__(self, message="", *args: object) -> None:
        super().__init__(f"Grupo {message} inexistente.")

class QuantidadeInsuficenteParaMovimentacao(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Quantidade insuficiente para a movimentação.")
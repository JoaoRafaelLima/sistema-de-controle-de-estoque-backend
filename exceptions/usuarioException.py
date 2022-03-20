


class UsuarioInexistente(Exception):
    def __init__(self) -> None:
        super().__init__("Usuário inexistente")


class LoginJaCadastrado(Exception):
    def __init__(self) -> None:
        super().__init__("Já existe um usuário com esse login")

import math

class Produto:
    def __init__(self, id: int, nome: str, categoria: str, preco: float, estoque: int):
        if type(id) is not int or id <= 0:
            raise ValueError("ID inválido")
        if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 100:
            raise ValueError("Nome inválido")
        if not isinstance(categoria, str) or not categoria.strip() or len(categoria.strip()) > 60:
            raise ValueError("Categoria inválida")
        if isinstance(preco, bool) or not isinstance(preco, (int, float)) or not math.isfinite(preco) or preco < 0:
            raise ValueError("Preço inválido")
        if type(estoque) is not int or estoque < 0:
            raise ValueError("Estoque inválido")
        self.id = id
        self.nome = nome.strip()
        self.categoria = categoria.strip()
        self.preco = round(float(preco), 2)
        self.estoque = estoque
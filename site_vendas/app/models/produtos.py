class Produto():
    def __init__(self, id: int, nome: str, categoria: str, preco: float, estoque: int):

        # Verificações de tipo de dados
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID inválido")

        if not isinstance(nome, str) or not nome.strip():
            raise ValueError("Nome inválido")

        if not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("Categoria inválida")

        if isinstance(preco, bool) or not isinstance(preco, (int, float)):
            raise ValueError("Preço deve ser numérico")

        if preco < 0:
            raise ValueError("Preço não pode ser negativo")

        if isinstance(estoque, bool) or not isinstance(estoque, int):
            raise ValueError("Estoque deve ser um número inteiro")

        if estoque < 0:
            raise ValueError("Estoque não pode ser um número negativo")
        
        self.id = id
        self.nome = nome.strip()
        self.categoria = categoria.strip()
        self.preco = preco
        self.estoque = estoque
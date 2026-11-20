from app.models.produtos import Produto
from pathlib import Path # Manipulação de caminhos de arquivos e dir de forma orientada a objetos
import json

class DataRecord:

    def __init__(self):
        self.produtos = []

        # Criação de um caminho absoluto para o arquivo produtos.json
        self.caminho_json = (Path(__file__).resolve().parent / "db" / "produtos.json")

        try:
            with open(self.caminho_json, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)

            self.produtos = [Produto(**data) for data in dados]

        except FileNotFoundError:
            self.produtos = []
            self.salvar_produtos()

    def work_with_parameter(self, parameter):
        try:
            id_produto = int(parameter)
        except (ValueError, TypeError):
            return None

        for produto in self.produtos:
            if produto.id == id_produto:
                return produto
            
        return None

    def salvar_produtos(self):
        dados = [
            {
                "id": produto.id,
                "nome": produto.nome,
                "categoria": produto.categoria,
                "preco": produto.preco,
                "estoque": produto.estoque
            }
            for produto in self.produtos
        ]

        with open(self.caminho_json, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)

    # Implementação do CRUD
    def adicionar_produto(self, nome, categoria, preco, estoque):
        novo_id = max((produto.id for produto in self.produtos), default=0) + 1 

        novo_produto = Produto(novo_id, nome, categoria, preco, estoque)

        self.produtos.append(novo_produto) # Adiciona objeto à lista

        self.salvar_produtos() # Atualiza JSON com o novo produto criado

        return novo_produto

    def atualizar_produto(self, id_produto, nome, categoria, preco, estoque):
        produto = self.work_with_parameter(id_produto)

        if produto is None:
            return False

        # Validação dos novos dados antes de atualizar o produto existente
        produto_atualizado = Produto(produto.id, nome, categoria, preco, estoque)

        produto.nome = produto_atualizado.nome
        produto.categoria = produto_atualizado.categoria
        produto.preco = produto_atualizado.preco
        produto.estoque = produto_atualizado.estoque

        self.salvar_produtos()
        return True

    def excluir_produto(self, id_produto):
        produto = self.work_with_parameter(id_produto)

        if produto is None:
            return False

        self.produtos.remove(produto)
        self.salvar_produtos()

        return True

    def listar_produtos(self):
        return self.produtos.copy()
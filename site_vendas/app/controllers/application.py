from bottle import template
from app.controllers.datarecord import DataRecord

class Application:
    def __init__(self, datarecord=None):
        self.datarecord = datarecord or DataRecord()

    def render(self, pagina, **contexto):
        if pagina not in ('inicio', 'produtos', 'catalogo', 'login', 'cadastro', 'conta', 'helper'):
            pagina = 'helper'
        if pagina in ('produtos', 'catalogo'):
            contexto['produtos'] = self.datarecord.listar_produtos()
        return template('app/views/html/' + pagina, **contexto)

    def cadastrar_produto(self, nome, categoria, preco, estoque):
        return self.datarecord.adicionar_produto(nome, categoria, preco, estoque)

    def buscar_produto(self, id_produto):
        return self.datarecord.work_with_parameter(id_produto)

    def atualizar_produto(self, id_produto, nome, categoria, preco, estoque):
        return self.datarecord.atualizar_produto(id_produto, nome, categoria, preco, estoque)

    def excluir_produto(self, id_produto):
        return self.datarecord.excluir_produto(id_produto)
from bottle import template # Carrega o arquivo em TLP e o converte para html
from app.controllers.datarecord import DataRecord

class Application(): # Organização de páginas

    def __init__(self):
        self.datarecord = DataRecord()

        self.pages = {
            'helper': self.helper,
            'inicio': self.inicio,
            'produtos': self.produtos
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content() # self.inicio, self.produtos

    def helper(self):
        return template('app/views/html/helper')

    def inicio(self):
        return template('app/views/html/inicio')

    def produtos(self):
        lista_produtos = self.datarecord.listar_produtos()

        return template('app/views/html/produtos', produtos=lista_produtos)

    def cadastrar_produto(self, nome, categoria, preco, estoque):
        return self.datarecord.adicionar_produto(nome, categoria, preco, estoque)

    def buscar_produto(self, id_produto):
        return self.datarecord.work_with_parameter(id_produto)

    def atualizar_produto(self, id_produto, nome, categoria, preco, estoque):
        return self.datarecord.atualizar_produto(id_produto, nome, categoria, preco, estoque)

    def excluir_produto(self, id_produto):
        return self.datarecord.excluir_produto(id_produto)

from bottle import template # Carrega o arquivo em TLP e o converte para html


class Application(): # Organização de páginas

    def __init__(self):
        self.pages = {
            'inicio': self.inicio,
            'produtos': self.produtos
        }


    def render(self,page):
       content = self.pages.get(page, self.helper)
       return content()


    def helper(self):
        return template('app/views/html/helper')

    def inicio(self):
        return template('app/views/html/inicio')

    def produtos(self):
        return template('app/views/html/produtos')

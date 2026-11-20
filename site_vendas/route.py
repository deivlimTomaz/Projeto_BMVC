from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response, HTTPError


app = Bottle()
ctl = Application()


#-----------------------------------------------------------------------------
# Rotas:

@app.route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root='./app/static')

@app.route('/helper')
def helper(info= None):
    return ctl.render('helper')

#-----------------------------------------------------------------------------
# Suas rotas aqui:

# Página inicial
@app.route('/')
def index():
    return redirect('/inicio')

@app.route('/inicio', methods=['GET']) # Registro de rota na aplicação
def action_pagina():
    return ctl.render('inicio') # Renderiza o template (ex.: arquivo html/tpl)

# READ - Listar produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return ctl.render('produtos')

# CREATE - Cadastrar produto
@app.route('/produtos/adicionar', method=['POST'])
def adicionar_produto():
    try:
        nome = request.forms.get('nome')
        categoria = request.forms.get('categoria')
        preco = float(request.forms.get('preco').replace(',', '.'))
        estoque = int(request.forms.get('estoque'))

        ctl.cadastrar_produto(nome, categoria, preco, estoque)

    except (ValueError, TypeError, AttributeError) as erro:
        raise HTTPError(400, f"Dados inválidos: {erro}")

    return redirect('/produtos')

# UPDATE - Atualizar produto
@app.route('/produtos/editar/<id_produto:int>', method=['POST'])
def editar_produto(id_produto):
    try:
        nome = request.forms.get('nome')
        categoria = request.forms.get('categoria')
        preco = float(request.forms.get('preco').replace(',', '.'))
        estoque = int(request.forms.get('estoque'))

        atualizado = ctl.atualizar_produto(id_produto, nome, categoria, preco, estoque)

        if not atualizado:
            raise HTTPError(404, "Produto não encontrado")

    except (ValueError, TypeError, AttributeError) as erro:
        raise HTTPError(400, f"Dados inválidos: {erro}")

    return redirect('/produtos')

# DELTE - Excluir produto
@app.route('/produtos/excluir/<id_produto:int>', method=['POST'])
def excluir_produto(id_produto):
    excluido = ctl.excluir_produto(id_produto)

    if not excluido:
        raise HTTPError(404, 'Produto não encontrado')

    return redirect('/produtos')
#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)

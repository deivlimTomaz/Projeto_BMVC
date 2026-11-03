from app.controllers.application import Application
from bottle import Bottle, route, run, request, static_file
from bottle import redirect, template, response


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
@app.route('/inicio', methods=['GET']) # Registro de rota na aplicação
def action_pagina():
    return ctl.render('inicio') # Renderiza o template (ex.: arquivo html/tpl)

# Página de busca de produtos
@app.route('/produtos', methods=['GET'])
def action_pagina():
    return ctl.render('produtos')

#-----------------------------------------------------------------------------


if __name__ == '__main__':

    run(app, host='0.0.0.0', port=8080, debug=True)

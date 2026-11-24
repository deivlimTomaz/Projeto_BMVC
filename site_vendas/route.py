import os
import secrets
from pathlib import Path
from bottle import Bottle, HTTPError, abort, redirect, request, response, run, static_file
from app.controllers.application import Application
from app.controllers.auth import Sessoes, UsuarioRepository

RAIZ = Path(__file__).resolve().parent
app = Bottle()
ctl = Application()
usuarios = UsuarioRepository()
sessoes = Sessoes()
COOKIE = 'bmvc_sessao'


def sessao():
    token = request.get_cookie(COOKIE)
    dados = sessoes.obter(token)
    if dados is None:
        token = sessoes.criar()
        dados = sessoes.obter(token)
        response.set_cookie(COOKIE, token, httponly=True, samesite='Strict', secure=os.getenv('BMVC_HTTPS') == '1', path='/')
    return token, dados


def usuario_atual():
    _, dados = sessao()
    identificador = dados['usuario_id']
    return usuarios.buscar_id(identificador) if identificador is not None else None


def proteger_csrf():
    _, dados = sessao()
    valor = request.forms.get('csrf', '')
    if not secrets.compare_digest(str(valor), dados['csrf']):
        abort(403, 'Formulário inválido (CSRF).')


def contexto(mensagem=''):
    _, dados = sessao()
    return {'usuario': usuario_atual(), 'csrf': dados['csrf'], 'mensagem': mensagem}


def gerente_obrigatorio():
    usuario = usuario_atual()
    if not usuario:
        abort(401, 'Faça login para continuar.')
    if usuario.papel != 'gerente':
        abort(403, 'Somente o gerente pode gerenciar produtos.')
    return usuario


def cliente_obrigatorio():
    usuario = usuario_atual()
    if not usuario:
        redirect('/login')
    return usuario


@app.get('/static/<filepath:path>')
def arquivos_estaticos(filepath):
    return static_file(filepath, root=str(RAIZ / 'app' / 'static'))


@app.get('/')
def raiz():
    return redirect('/inicio')


@app.get('/inicio')
def inicio():
    return ctl.render('inicio', **contexto())


@app.get('/helper')
def helper():
    return ctl.render('helper', **contexto())


@app.get('/catalogo')
def catalogo():
    return ctl.render('catalogo', **contexto())


@app.get('/produtos')
def produtos():
    gerente_obrigatorio()
    return ctl.render('produtos', **contexto())


def dados_produto():
    nome = request.forms.get('nome', '')
    categoria = request.forms.get('categoria', '')
    preco_texto = request.forms.get('preco', '').strip().replace(',', '.')
    estoque_texto = request.forms.get('estoque', '').strip()
    return nome, categoria, float(preco_texto), int(estoque_texto)


@app.post('/produtos/adicionar')
def adicionar_produto():
    gerente_obrigatorio()
    proteger_csrf()
    try:
        ctl.cadastrar_produto(*dados_produto())
    except (ValueError, TypeError, AttributeError) as erro:
        abort(400, str(erro))
    return redirect('/produtos')


@app.post('/produtos/editar/<id_produto:int>')
def editar_produto(id_produto):
    gerente_obrigatorio()
    proteger_csrf()
    try:
        alterado = ctl.atualizar_produto(id_produto, *dados_produto())
    except (ValueError, TypeError, AttributeError) as erro:
        abort(400, str(erro))
    if not alterado:
        abort(404, 'Produto não encontrado.')
    return redirect('/produtos')


@app.post('/produtos/excluir/<id_produto:int>')
def excluir_produto(id_produto):
    gerente_obrigatorio()
    proteger_csrf()
    if not ctl.excluir_produto(id_produto):
        abort(404, 'Produto não encontrado.')
    return redirect('/produtos')


@app.get('/cadastro')
def cadastro():
    if usuario_atual():
        return redirect('/conta')
    return ctl.render('cadastro', **contexto())


@app.post('/cadastro')
def cadastrar_cliente():
    proteger_csrf()
    if usuario_atual():
        abort(403, 'Saia da conta antes de cadastrar outra.')
    nome = request.forms.get('nome', '')
    email = request.forms.get('email', '')
    senha = request.forms.get('senha', '')
    confirmacao = request.forms.get('confirmacao', '')
    if senha != confirmacao:
        return ctl.render('cadastro', **contexto('As senhas não coincidem.'))
    try:
        usuarios.criar(nome, email, senha)  # cadastro público sempre cria cliente
    except ValueError as erro:
        return ctl.render('cadastro', **contexto(str(erro)))
    return redirect('/login?criado=1')


@app.get('/login')
def login():
    if usuario_atual():
        return redirect('/conta')
    mensagem = 'Conta criada. Faça login.' if request.query.get('criado') == '1' else ''
    return ctl.render('login', **contexto(mensagem))


@app.post('/login')
def autenticar():
    proteger_csrf()
    usuario = usuarios.autenticar(request.forms.get('email', ''), request.forms.get('senha', ''))
    if not usuario:
        return ctl.render('login', **contexto('E-mail ou senha inválidos.'))
    token_antigo, _ = sessao()
    sessoes.remover(token_antigo)
    token_novo = sessoes.criar(usuario.id)
    response.set_cookie(COOKIE, token_novo, httponly=True, samesite='Strict', secure=os.getenv('BMVC_HTTPS') == '1', path='/')
    return redirect('/produtos' if usuario.papel == 'gerente' else '/conta')


@app.get('/conta')
def conta():
    cliente_obrigatorio()
    return ctl.render('conta', **contexto())


@app.post('/logout')
def logout():
    proteger_csrf()
    token, _ = sessao()
    sessoes.remover(token)
    response.delete_cookie(COOKIE, path='/')
    return redirect('/inicio')


if __name__ == '__main__':
    run(app, host='0.0.0.0', port=8080, debug=False, reloader=False)
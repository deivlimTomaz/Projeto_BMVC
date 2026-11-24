"""Execute na raiz site_vendas: python criar_gerente.py"""
from getpass import getpass
from app.controllers.auth import UsuarioRepository


def main():
    print('Cadastro local de gerente. Não exponha este comando pela web.')
    nome = input('Nome: ').strip()
    email = input('E-mail: ').strip()
    senha = getpass('Senha (mínimo 10 caracteres): ')
    confirmacao = getpass('Confirme a senha: ')
    if senha != confirmacao:
        raise SystemExit('As senhas não coincidem.')
    try:
        usuario = UsuarioRepository().criar(nome, email, senha, 'gerente', admin=True)
    except (ValueError, PermissionError) as erro:
        raise SystemExit(str(erro))
    print(f'Gerente criado: {usuario.email} (ID {usuario.id})')


if __name__ == '__main__':
    main()

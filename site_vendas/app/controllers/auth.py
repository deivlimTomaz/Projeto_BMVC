import hashlib
import hmac
import json
import os
import re
import secrets
import tempfile
import threading
from pathlib import Path
from app.models.usuario import Usuario

DB_USUARIOS = Path(__file__).resolve().parent / 'db' / 'usuarios.json'
ITERACOES = 260_000


def hash_senha(senha):
    salt = secrets.token_bytes(16)
    chave = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, ITERACOES)
    return f'pbkdf2_sha256${ITERACOES}${salt.hex()}${chave.hex()}'


def verificar_senha(senha, salvo):
    try:
        algoritmo, rodadas, salt, chave = salvo.split('$')
        if algoritmo != 'pbkdf2_sha256' or not 200_000 <= int(rodadas) <= 2_000_000:
            return False
        calculado = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), bytes.fromhex(salt), int(rodadas))
        return hmac.compare_digest(calculado, bytes.fromhex(chave))
    except (ValueError, TypeError, AttributeError):
        return False


class UsuarioRepository:
    def __init__(self, caminho=None):
        self.caminho = Path(caminho) if caminho else DB_USUARIOS
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
        if not self.caminho.exists():
            self._salvar([])

    def _ler(self):
        dados = json.loads(self.caminho.read_text(encoding='utf-8'))
        if not isinstance(dados, list):
            raise ValueError('Banco de usuários inválido')
        return [Usuario(**item) for item in dados]

    def _salvar(self, usuarios):
        fd, nome = tempfile.mkstemp(prefix='.usuarios_', dir=self.caminho.parent)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as arquivo:
                json.dump([vars(u) for u in usuarios], arquivo, indent=2, ensure_ascii=False)
            os.chmod(nome, 0o600)
            os.replace(nome, self.caminho)
        finally:
            if os.path.exists(nome):
                os.unlink(nome)

    def buscar_email(self, email):
        email = (email or '').strip().casefold()
        with self._lock:
            return next((u for u in self._ler() if u.email == email), None)

    def buscar_id(self, id_usuario):
        with self._lock:
            return next((u for u in self._ler() if u.id == id_usuario), None)

    def criar(self, nome, email, senha, papel='cliente', *, admin=False):
        nome = (nome or '').strip()
        email = (email or '').strip().casefold()
        if not 2 <= len(nome) <= 80:
            raise ValueError('Nome deve conter entre 2 e 80 caracteres')
        if not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email) or len(email) > 254:
            raise ValueError('E-mail inválido')
        if not isinstance(senha, str) or len(senha) < 10 or len(senha) > 256:
            raise ValueError('A senha deve conter entre 10 e 256 caracteres')
        if papel not in ('cliente', 'gerente') or (papel == 'gerente' and not admin):
            raise PermissionError('Perfil não autorizado')
        with self._lock:
            usuarios = self._ler()
            if any(u.email == email for u in usuarios):
                raise ValueError('E-mail já cadastrado')
            novo = Usuario(max((u.id for u in usuarios), default=0) + 1, nome, email, hash_senha(senha), papel)
            usuarios.append(novo)
            self._salvar(usuarios)
            return novo

    def autenticar(self, email, senha):
        usuario = self.buscar_email(email)
        if usuario and verificar_senha(senha or '', usuario.senha_hash):
            return usuario
        return None


class Sessoes:
    """Sessões locais em memória. Reiniciar o servidor invalida logins."""
    def __init__(self):
        self.dados = {}
        self.lock = threading.RLock()

    def obter(self, token):
        with self.lock:
            return self.dados.get(token)

    def criar(self, id_usuario=None):
        token = secrets.token_urlsafe(32)
        with self.lock:
            self.dados[token] = {'usuario_id': id_usuario, 'csrf': secrets.token_urlsafe(32)}
        return token

    def remover(self, token):
        with self.lock:
            self.dados.pop(token, None)

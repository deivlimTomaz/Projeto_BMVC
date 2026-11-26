"""Persistência SQLite de produtos e pedidos do BMVC Nível 4."""
import sqlite3
from pathlib import Path
from app.models.produtos import Produto

DB_PADRAO = Path(__file__).resolve().parent / 'db' / 'vendas.db'


class EstoqueInsuficiente(ValueError):
    pass

# Gerenciamento de produtos
class SQLiteStore:
    def __init__(self, caminho_db=None):
        self.caminho_db = Path(caminho_db) if caminho_db is not None else DB_PADRAO
        self.caminho_db.parent.mkdir(parents=True, exist_ok=True)
        with self._conectar() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    preco_centavos INTEGER NOT NULL CHECK (preco_centavos >= 0),
                    estoque INTEGER NOT NULL CHECK (estoque >= 0)
                );
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario_id INTEGER NOT NULL,
                    total_centavos INTEGER NOT NULL CHECK (total_centavos >= 0),
                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                CREATE TABLE IF NOT EXISTS itens_pedido (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
                    produto_id INTEGER NOT NULL,
                    nome_produto TEXT NOT NULL,
                    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                    preco_unitario_centavos INTEGER NOT NULL CHECK (preco_unitario_centavos >= 0)
                );
            ''')

    def _conectar(self):
        conn = sqlite3.connect(self.caminho_db, timeout=15)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute('PRAGMA busy_timeout = 15000')
        return conn

    @staticmethod
    def _produto(linha):
        return Produto(linha['id'], linha['nome'], linha['categoria'],
                       linha['preco_centavos'] / 100, linha['estoque'])

    @staticmethod
    def _centavos(preco):
        # Produto já valida e arredonda o preço para duas casas decimais.
        return round(preco * 100)

    def listar_produtos(self):
        with self._conectar() as conn:
            linhas = conn.execute('SELECT * FROM produtos ORDER BY id').fetchall()
        return [self._produto(linha) for linha in linhas]

    def work_with_parameter(self, parameter):
        try:
            identificador = int(parameter)
        except (TypeError, ValueError):
            return None
        with self._conectar() as conn:
            linha = conn.execute('SELECT * FROM produtos WHERE id = ?', (identificador,)).fetchone()
        return self._produto(linha) if linha else None

    def adicionar_produto(self, nome, categoria, preco, estoque):
        validado = Produto(1, nome, categoria, preco, estoque)
        with self._conectar() as conn:
            cursor = conn.execute(
                'INSERT INTO produtos (nome, categoria, preco_centavos, estoque) VALUES (?, ?, ?, ?)',
                (validado.nome, validado.categoria, self._centavos(validado.preco), validado.estoque)
            )
            novo_id = cursor.lastrowid
        return self.work_with_parameter(novo_id)

    def atualizar_produto(self, id_produto, nome, categoria, preco, estoque):
        try:
            identificador = int(id_produto)
        except (TypeError, ValueError):
            return False
        validado = Produto(identificador, nome, categoria, preco, estoque)
        with self._conectar() as conn:
            cursor = conn.execute('''
                UPDATE produtos SET nome = ?, categoria = ?, preco_centavos = ?, estoque = ?
                WHERE id = ?
            ''', (validado.nome, validado.categoria, self._centavos(validado.preco),
                  validado.estoque, identificador))
        return cursor.rowcount > 0

    def excluir_produto(self, id_produto):
        try:
            identificador = int(id_produto)
        except (TypeError, ValueError):
            return False
        with self._conectar() as conn:
            cursor = conn.execute('DELETE FROM produtos WHERE id = ?', (identificador,))
        return cursor.rowcount > 0

    def confirmar_pedido(self, usuario_id, itens):
        """itens: {produto_id: quantidade}. Confirma tudo ou nada."""
        if type(usuario_id) is not int or usuario_id <= 0:
            raise ValueError('Usuário inválido')
        if not isinstance(itens, dict) or not itens:
            raise ValueError('Carrinho vazio')
        normalizados = {}
        for produto_id, quantidade in itens.items():
            if type(quantidade) is not int or quantidade <= 0:
                raise ValueError('Quantidade inválida')
            try:
                identificador = int(produto_id)
            except (ValueError, TypeError):
                raise ValueError('Produto inválido') from None
            if identificador <= 0 or identificador in normalizados:
                raise ValueError('Produto inválido ou duplicado')
            normalizados[identificador] = quantidade

        conn = self._conectar()
        try:
            conn.execute('BEGIN IMMEDIATE')
            linhas = []
            total = 0
            for identificador, quantidade in sorted(normalizados.items()):
                linha = conn.execute('SELECT * FROM produtos WHERE id = ?', (identificador,)).fetchone()
                if linha is None or linha['estoque'] < quantidade:
                    raise EstoqueInsuficiente(f'Estoque insuficiente para o produto {identificador}')
                linhas.append((linha, quantidade))
                total += linha['preco_centavos'] * quantidade
            cursor = conn.execute(
                'INSERT INTO pedidos (usuario_id, total_centavos) VALUES (?, ?)',
                (usuario_id, total)
            )
            pedido_id = cursor.lastrowid
            for linha, quantidade in linhas:
                conn.execute('''
                    UPDATE produtos SET estoque = estoque - ? WHERE id = ? AND estoque >= ?
                ''', (quantidade, linha['id'], quantidade))
                conn.execute('''
                    INSERT INTO itens_pedido
                    (pedido_id, produto_id, nome_produto, quantidade, preco_unitario_centavos)
                    VALUES (?, ?, ?, ?, ?)
                ''', (pedido_id, linha['id'], linha['nome'], quantidade, linha['preco_centavos']))
            conn.commit()
            return pedido_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

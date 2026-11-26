"""Migração explícita e conservadora do JSON do Nível 3 para SQLite.

Execute na raiz site_vendas, após criar um backup de produtos.json.
Não sobrescreve produtos existentes no banco.
"""
import json
from pathlib import Path
from app.controllers.sqlite_store import SQLiteStore
from app.models.produtos import Produto


def migrar(caminho_json=None, caminho_db=None):
    arquivo = Path(caminho_json) if caminho_json else Path('app/controllers/db/produtos.json')
    dados = json.loads(arquivo.read_text(encoding='utf-8'))
    if not isinstance(dados, list):
        raise ValueError('JSON precisa conter uma lista')
    produtos = [Produto(**registro) for registro in dados]
    ids = [produto.id for produto in produtos]
    if len(ids) != len(set(ids)):
        raise ValueError('IDs duplicados no JSON')

    store = SQLiteStore(caminho_db)
    conn = store._conectar()
    try:
        conn.execute('BEGIN IMMEDIATE')
        if conn.execute('SELECT COUNT(*) FROM produtos').fetchone()[0]:
            raise RuntimeError('Migração cancelada: o banco já contém produtos')
        for produto in produtos:
            conn.execute('''
                INSERT INTO produtos (id, nome, categoria, preco_centavos, estoque)
                VALUES (?, ?, ?, ?, ?)
            ''', (produto.id, produto.nome, produto.categoria,
                  store._centavos(produto.preco), produto.estoque))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print(f'Migração concluída: {len(produtos)} produtos importados.')


if __name__ == '__main__':
    migrar()

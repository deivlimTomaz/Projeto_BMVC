import tempfile
import threading
from pathlib import Path
from app.controllers.sqlite_store import SQLiteStore, EstoqueInsuficiente


def executar():
    with tempfile.TemporaryDirectory() as tmp:
        store = SQLiteStore(Path(tmp) / 'vendas.db')
        p = store.adicionar_produto('Sabonete Líquido', 'Cuidados', 5.00, 1)
        assert p.id == 1
        assert store.work_with_parameter(p.id).nome == 'Sabonete Líquido'
        assert len(store.listar_produtos()) == 1
        assert store.atualizar_produto(p.id, 'Sabonete Líquido', 'Cuidados', 6.50, 1)
        assert store.work_with_parameter(p.id).preco == 6.50

        resultados = []
        trava = threading.Lock()
        barreira = threading.Barrier(2)

        def comprar(usuario_id):
            barreira.wait()
            try:
                pedido = store.confirmar_pedido(usuario_id, {p.id: 1})
                resultado = ('ok', pedido)
            except EstoqueInsuficiente:
                resultado = ('sem_estoque', usuario_id)
            with trava:
                resultados.append(resultado)

        t1 = threading.Thread(target=comprar, args=(1,))
        t2 = threading.Thread(target=comprar, args=(2,))
        t1.start(); t2.start(); t1.join(); t2.join()
        assert sorted(x[0] for x in resultados) == ['ok', 'sem_estoque'], resultados
        assert store.work_with_parameter(p.id).estoque == 0

        with store._conectar() as conn:
            assert conn.execute('SELECT COUNT(*) FROM pedidos').fetchone()[0] == 1
            assert conn.execute('SELECT total_centavos FROM pedidos').fetchone()[0] == 650
        assert store.excluir_produto(p.id)
        assert store.work_with_parameter(p.id) is None
        print('SQLite: CRUD, atomicidade e concorrência passaram.')


if __name__ == '__main__':
    executar()


import tempfile
from pathlib import Path

from app.controllers.application import Application
from app.controllers.datarecord import DataRecord


with tempfile.TemporaryDirectory() as pasta:
    caminho = Path(pasta) / "produtos_teste.json"
    caminho.write_text("[]", encoding="utf-8")

    app = Application()

    # Substitui o DataRecord pelo de teste
    db_teste = DataRecord()
    db_teste.caminho_json = caminho
    db_teste.produtos = []

    app.datarecord = db_teste

    # CREATE
    produto = app.cadastrar_produto(
        "Sabonete", "Higiene", 12.50, 20
    )
    assert produto.id == 1

    # READ
    encontrado = app.buscar_produto(produto.id)
    assert encontrado.nome == "Sabonete"

    # UPDATE
    atualizado = app.atualizar_produto(
        produto.id, "Sabonete Líquido", "Higiene", 18.90, 15
    )
    assert atualizado is True
    assert app.buscar_produto(produto.id).preco == 18.90

    # DELETE
    excluido = app.excluir_produto(produto.id)
    assert excluido is True
    assert app.buscar_produto(produto.id) is None

    print("Integração Application + DataRecord funcionando.")

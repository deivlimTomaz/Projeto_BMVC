import tempfile
from pathlib import Path

from app.controllers.datarecord import DataRecord


with tempfile.TemporaryDirectory() as pasta:
    caminho_teste = Path(pasta) / "produtos_teste.json"
    caminho_teste.write_text("[]", encoding="utf-8")

    db = DataRecord()
    db.caminho_json = caminho_teste
    db.produtos = []

    # CREATE
    produto = db.adicionar_produto(
        "Perfume", "Perfumaria", 120.00, 10
    )
    assert produto.id == 1

    # READ
    encontrado = db.work_with_parameter(produto.id)
    assert encontrado.nome == "Perfume"
    assert len(db.listar_produtos()) == 1

    # UPDATE
    resultado = db.atualizar_produto(
        produto.id, "Perfume Premium", "Perfumaria", 150.00, 5
    )
    assert resultado is True
    assert db.work_with_parameter(produto.id).preco == 150.00

    # Persistência
    db_recarregado = DataRecord()
    db_recarregado.caminho_json = caminho_teste

    # Recarrega os dados do arquivo temporário
    import json
    from app.models.produtos import Produto

    with open(caminho_teste, encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    db_recarregado.produtos = [Produto(**dado) for dado in dados]

    assert db_recarregado.work_with_parameter(produto.id).nome == "Perfume Premium"

    # DELETE
    assert db.excluir_produto(produto.id) is True
    assert db.work_with_parameter(produto.id) is None
    assert db.excluir_produto(produto.id) is False

    print("CRUD completo: todos os testes passaram.")

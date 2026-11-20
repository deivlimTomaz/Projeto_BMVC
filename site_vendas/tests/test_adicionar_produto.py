from app.controllers.datarecord import DataRecord

db = DataRecord()

produto = db.adicionar_produto(
    "Condicionador",
    "Capilares",
    35.90,
    10
)

assert produto.nome == "Condicionador"
assert produto.preco == 35.90

db2 = DataRecord()
assert db2.work_with_parameter(produto.id) is not None

print("Cadastro e persistência funcionando.")

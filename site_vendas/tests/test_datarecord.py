from app.controllers.datarecord import DataRecord
from app.models.produtos import Produto

db = DataRecord()

# Criar um produto em memória
produto = Produto(1, "Shampoo", "Capilares", 30.00, 5)

db.produtos.append(produto)

# Salvar no JSON
db.salvar_produtos()

# Recarregar os produtos do arquivo
db2 = DataRecord()

# Buscar pelo ID
resultado = db2.work_with_parameter(1)

assert resultado is not None
assert resultado.nome == "Shampoo"
assert resultado.preco == 30.00
assert resultado.estoque == 5

print("Teste de leitura, gravação e busca concluído.")
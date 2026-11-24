import json
import os
import tempfile
from pathlib import Path
from app.models.produtos import Produto

DB_PADRAO = Path(__file__).resolve().parent / 'db' / 'produtos.json'

class DataRecord:
    def __init__(self, caminho_json=None):
        self.caminho_json = Path(caminho_json) if caminho_json else DB_PADRAO
        self.caminho_json.parent.mkdir(parents=True, exist_ok=True)
        if not self.caminho_json.exists():
            self.caminho_json.write_text('[]', encoding='utf-8')
        dados = json.loads(self.caminho_json.read_text(encoding='utf-8'))
        if not isinstance(dados, list):
            raise ValueError('Arquivo de produtos inválido')
        self.produtos = [Produto(**d) for d in dados]

    def salvar_produtos(self):
        dados = [vars(p) for p in self.produtos]
        fd, temporario = tempfile.mkstemp(dir=self.caminho_json.parent, prefix='.produtos_', suffix='.tmp')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            os.replace(temporario, self.caminho_json)
        finally:
            if os.path.exists(temporario):
                os.unlink(temporario)

    def listar_produtos(self):
        return self.produtos.copy()

    def work_with_parameter(self, parameter):
        try:
            produto_id = int(parameter)
        except (ValueError, TypeError):
            return None
        return next((p for p in self.produtos if p.id == produto_id), None)

    def adicionar_produto(self, nome, categoria, preco, estoque):
        novo_id = max((p.id for p in self.produtos), default=0) + 1
        produto = Produto(novo_id, nome, categoria, preco, estoque)
        self.produtos.append(produto)
        self.salvar_produtos()
        return produto

    def atualizar_produto(self, id_produto, nome, categoria, preco, estoque):
        anterior = self.work_with_parameter(id_produto)
        if anterior is None:
            return False
        novo = Produto(anterior.id, nome, categoria, preco, estoque)
        indice = self.produtos.index(anterior)
        self.produtos[indice] = novo
        self.salvar_produtos()
        return True

    def excluir_produto(self, id_produto):
        produto = self.work_with_parameter(id_produto)
        if produto is None:
            return False
        self.produtos.remove(produto)
        self.salvar_produtos()
        return True
import tempfile
import unittest

from pathlib import Path

from app.controllers.application import Application
from app.controllers.datarecord import DataRecord


class TestIntegracaoSQLite(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()

        self.caminho_db = (
            Path(self.temp.name) / "vendas_teste.db"
        )

        self.datarecord = DataRecord(self.caminho_db)

        self.app = Application(
            datarecord=self.datarecord
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_cadastro(self):
        produto = self.app.cadastrar_produto(
            "Sabonete Líquido",
            "Cuidados",
            15.90,
            10
        )

        self.assertEqual(
            produto.nome,
            "Sabonete Líquido"
        )

        self.assertEqual(produto.estoque, 10)

    def test_listagem(self):
        self.app.cadastrar_produto(
            "Shampoo",
            "Capilares",
            30.00,
            5
        )

        produtos = self.datarecord.listar_produtos()

        self.assertEqual(len(produtos), 1)
        self.assertEqual(produtos[0].nome, "Shampoo")

    def test_atualizacao(self):
        produto = self.app.cadastrar_produto(
            "Condicionador",
            "Capilares",
            25.00,
            10
        )

        resultado = self.app.atualizar_produto(
            produto.id,
            "Condicionador Premium",
            "Capilares",
            35.00,
            8
        )

        self.assertTrue(resultado)

        atualizado = self.app.buscar_produto(produto.id)

        self.assertEqual(
            atualizado.nome,
            "Condicionador Premium"
        )

        self.assertEqual(atualizado.estoque, 8)

    def test_exclusao(self):
        produto = self.app.cadastrar_produto(
            "Perfume",
            "Perfumaria",
            120.00,
            3
        )

        resultado = self.app.excluir_produto(produto.id)

        self.assertTrue(resultado)

        self.assertIsNone(
            self.app.buscar_produto(produto.id)
        )

    def test_persistencia(self):
        produto = self.app.cadastrar_produto(
            "Óleo de Amêndoas",
            "Cuidados",
            20.00,
            15
        )

        outro_datarecord = DataRecord(self.caminho_db)

        recuperado = outro_datarecord.work_with_parameter(
            produto.id
        )

        self.assertIsNotNone(recuperado)

        self.assertEqual(
            recuperado.nome,
            "Óleo de Amêndoas"
        )

        self.assertEqual(recuperado.estoque, 15)


if __name__ == "__main__":
    unittest.main()

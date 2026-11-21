
<!DOCTYPE html>
<html lang="pt-BR">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Produtos | Site de Vendas</title>

    <link rel="stylesheet" href="/static/css/produtos.css">
    <script src="/static/js/produtos.js" defer></script>
</head>

<body>

    <header>
        <h1>Gerenciamento de Produtos</h1>

        <nav>
            <a href="/inicio">Início</a>
            <a href="/produtos">Produtos</a>
        </nav>
    </header>

    <main>

        <!-- CREATE: CADASTRAR PRODUTO -->
        <section>
            <h2>Cadastrar produto</h2>

            <form action="/produtos/adicionar"
                  method="POST"
                  class="form-cadastro">

                <div class="campo">
                    <label for="nome">Nome:</label>
                    <input
                        type="text"
                        id="nome"
                        name="nome"
                        required>
                </div>

                <div class="campo">
                    <label for="categoria">Categoria:</label>
                    <input
                        type="text"
                        id="categoria"
                        name="categoria"
                        required>
                </div>

                <div class="campo">
                    <label for="preco">Preço:</label>
                    <input
                        type="number"
                        id="preco"
                        name="preco"
                        min="0"
                        step="0.01"
                        required>
                </div>

                <div class="campo">
                    <label for="estoque">Estoque:</label>
                    <input
                        type="number"
                        id="estoque"
                        name="estoque"
                        min="0"
                        step="1"
                        required>
                </div>

                <button type="submit" class="botao-cadastrar">
                    Cadastrar
                </button>

            </form>
        </section>

        <!-- READ: LISTAR PRODUTOS -->
        <section>
            <h2>Produtos cadastrados</h2>

            % if not produtos:

                <p class="mensagem-vazia">
                    Nenhum produto cadastrado.
                </p>

            % else:

                <!-- BUSCA DINÂMICA -->
                <input
                    type="search"
                    id="buscar-produto"
                    class="busca-produto"
                    placeholder="Buscar por nome ou categoria..."
                    aria-label="Buscar produtos">

                <div class="tabela-container">

                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Nome</th>
                                <th>Categoria</th>
                                <th>Preço</th>
                                <th>Estoque</th>
                                <th>Ações</th>
                            </tr>
                        </thead>

                        <tbody>

                            % for produto in produtos:

                            <tr class="linha-produto"
                                data-nome="{{produto.nome.lower()}}"
                                data-categoria="{{produto.categoria.lower()}}">

                                <td>{{produto.id}}</td>

                                <td>{{produto.nome}}</td>

                                <td>{{produto.categoria}}</td>

                                <td>
                                    R$ {{f"{produto.preco:.2f}".replace(".", ",")}}
                                </td>

                                <td>{{produto.estoque}}</td>

                                <td class="coluna-acoes">

                                    <!-- UPDATE: EDITAR PRODUTO -->
                                    <details>
                                        <summary>Editar</summary>

                                        <form
                                            action="/produtos/editar/{{produto.id}}"
                                            method="POST"
                                            class="form-edicao">

                                            <label>Nome:</label>
                                            <input
                                                type="text"
                                                name="nome"
                                                value="{{produto.nome}}"
                                                required>

                                            <label>Categoria:</label>
                                            <input
                                                type="text"
                                                name="categoria"
                                                value="{{produto.categoria}}"
                                                required>

                                            <label>Preço:</label>
                                            <input
                                                type="number"
                                                name="preco"
                                                min="0"
                                                step="0.01"
                                                value="{{f'{produto.preco:.2f}'}}"
                                                required>

                                            <label>Estoque:</label>
                                            <input
                                                type="number"
                                                name="estoque"
                                                min="0"
                                                step="1"
                                                value="{{produto.estoque}}"
                                                required>

                                            <button
                                                type="submit"
                                                class="botao-salvar">
                                                Salvar alterações
                                            </button>

                                        </form>
                                    </details>

                                    <!-- DELETE: EXCLUIR PRODUTO -->
                                    <form
                                        action="/produtos/excluir/{{produto.id}}"
                                        method="POST"
                                        class="form-excluir"
                                        data-nome="{{produto.nome}}">

                                        <button
                                            type="submit"
                                            class="botao-excluir">
                                            Excluir
                                        </button>

                                    </form>

                                </td>
                            </tr>

                            % end

                        </tbody>
                    </table>

                </div>

                <p id="sem-resultados"
                   class="mensagem-vazia"
                   hidden>
                    Nenhum produto corresponde à pesquisa.
                </p>

            % end

        </section>

    </main>

</body>
</html>

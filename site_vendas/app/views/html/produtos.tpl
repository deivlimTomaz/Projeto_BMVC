<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <title>
      Gerenciar produtos | Beleza que faz bem
    </title>
    <link href="/static/css/estilos_site.css" rel="stylesheet"/>
    <script defer="" src="/static/js/produtos.js">
    </script>
  </head>
  <body class="pagina-interna">
    <header class="topo-site">
      <a class="marca" href="/inicio">
        Beleza que faz bem
      </a>
      <nav class="menu-principal">
        <a href="/catalogo">
          Catálogo
        </a>
        <a href="/conta">
          Minha conta
        </a>
        <form action="/logout" class="inline-form" method="post">
          <input name="csrf" type="hidden" value="{{csrf}}"/>
          <button class="btn-discreto">
            Sair
          </button>
        </form>
      </nav>
    </header>
    <main class="container">
      <div class="titulo-pagina">
        <span class="sobrelinha">
          ÁREA RESTRITA
        </span>
        <h1>
          Gerenciamento de produtos
        </h1>
        <p>
          Somente gerentes podem cadastrar, editar e excluir registros.
        </p>
      </div>
      <section class="painel">
        <h2>
          Cadastrar produto
        </h2>
        <form action="/produtos/adicionar" class="form-cadastro" method="post">
          <input name="csrf" type="hidden" value="{{csrf}}"/>
          <div class="campo">
            <label for="nome">
              Nome
            </label>
            <input id="nome" maxlength="100" name="nome" required="" type="text"/>
          </div>
          <div class="campo">
            <label for="categoria">
              Categoria
            </label>
            <input id="categoria" maxlength="60" name="categoria" required="" type="text"/>
          </div>
          <div class="campo">
            <label for="preco">
              Preço
            </label>
            <input id="preco" min="0" name="preco" required="" step="0.01" type="number"/>
          </div>
          <div class="campo">
            <label for="estoque">
              Estoque
            </label>
            <input id="estoque" min="0" name="estoque" required="" step="1" type="number"/>
          </div>
          <button class="botao" type="submit">
            Cadastrar produto
          </button>
        </form>
      </section>
      <section class="painel">
        <h2>
          Produtos cadastrados
        </h2>
        % if not produtos:
        <p>
          Nenhum produto cadastrado.
        </p>
        % else:
        <label class="sr-only" for="buscar-produto">
          Buscar produtos
        </label>
        <input class="campo-busca" id="buscar-produto" placeholder="Buscar por nome ou categoria" type="search"/>
        <div class="tabela-container">
          <table>
            <thead>
              <tr>
                <th>
                  ID
                </th>
                <th>
                  Nome
                </th>
                <th>
                  Categoria
                </th>
                <th>
                  Preço
                </th>
                <th>
                  Estoque
                </th>
                <th>
                  Ações
                </th>
              </tr>
            </thead>
            <tbody>
              % for produto in produtos:
              <tr class="linha-produto" data-categoria="{{produto.categoria.casefold()}}" data-nome="{{produto.nome.casefold()}}">
                <td>
                  {{produto.id}}
                </td>
                <td>
                  {{produto.nome}}
                </td>
                <td>
                  {{produto.categoria}}
                </td>
                <td>
                  R$ {{f'{produto.preco:.2f}'.replace('.', ',')}}
                </td>
                <td>
                  {{produto.estoque}}
                </td>
                <td class="coluna-acoes">
                  <details>
                    <summary>
                      Editar
                    </summary>
                    <form action="/produtos/editar/{{produto.id}}" class="form-edicao" method="post">
                      <input name="csrf" type="hidden" value="{{csrf}}"/>
                      <label>
                        Nome
                        <input maxlength="100" name="nome" required="" value="{{produto.nome}}"/>
                      </label>
                      <label>
                        Categoria
                        <input maxlength="60" name="categoria" required="" value="{{produto.categoria}}"/>
                      </label>
                      <label>
                        Preço
                        <input min="0" name="preco" required="" step="0.01" type="number" value="{{f'{produto.preco:.2f}'}}"/>
                      </label>
                      <label>
                        Estoque
                        <input min="0" name="estoque" required="" step="1" type="number" value="{{produto.estoque}}"/>
                      </label>
                      <button class="botao" type="submit">
                        Salvar alterações
                      </button>
                    </form>
                  </details>
                  <form action="/produtos/excluir/{{produto.id}}" class="form-excluir" data-nome="{{produto.nome}}" method="post">
                    <input name="csrf" type="hidden" value="{{csrf}}"/>
                    <button class="botao botao-perigo" type="submit">
                      Excluir
                    </button>
                  </form>
                </td>
              </tr>
              % end
            </tbody>
          </table>
        </div>
        <p hidden="" id="sem-resultados">
          Nenhum produto corresponde à pesquisa.
        </p>
        % end
      </section>
    </main>
  </body>
</html>
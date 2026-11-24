<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <title>
      Minha conta | Beleza que faz bem
    </title>
    <link href="/static/css/estilos_site.css" rel="stylesheet"/>
  </head>
  <body class="pagina-interna">
    <header class="topo-site">
      <a class="marca" href="/inicio">
        Beleza que faz bem
      </a>
      <nav class="menu-principal">
        <a href="/inicio">
          Início
        </a>
        <a href="/catalogo">
          Catálogo
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
          ACESSO RESTRITO
        </span>
        <h1>
          Minha conta
        </h1>
        <p>
          Informações do usuário autenticado.
        </p>
      </div>
      <section class="painel painel-conta">
        <h2>
          Dados da conta
        </h2>
        <dl>
          <dt>
            Nome
          </dt>
          <dd>
            {{usuario.nome}}
          </dd>
          <dt>
            E-mail
          </dt>
          <dd>
            {{usuario.email}}
          </dd>
          <dt>
            Perfil
          </dt>
          <dd>
            {{'Gerente' if usuario.papel == 'gerente' else 'Cliente'}}
          </dd>
        </dl>
        <div class="acoes-inicio">
          <a class="botao" href="/catalogo">
            Ver catálogo
          </a>
          % if usuario.papel == 'gerente':
          <a class="botao botao-secundario" href="/produtos">
            Gerenciar produtos
          </a>
          % end
        </div>
      </section>
    </main>
  </body>
</html>
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <title>
      Entrar | Beleza que faz bem
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
      </nav>
    </header>
    <main class="area-auth">
      <section class="painel">
        <span class="sobrelinha">
          SUA CONTA
        </span>
        <h1>
          Entrar
        </h1>
        <p>
          Acesse seus dados ou a área de gerenciamento, conforme seu perfil.
        </p>
        % if mensagem:
        <p class="alerta" role="status">
          {{mensagem}}
        </p>
        % end
        <form action="/login" class="form-vertical" method="post">
          <input name="csrf" type="hidden" value="{{csrf}}"/>
          <label>
            E-mail
            <input autocomplete="username" name="email" required="" type="email"/>
          </label>
          <label>
            Senha
            <input autocomplete="current-password" name="senha" required="" type="password"/>
          </label>
          <button class="botao" type="submit">
            Entrar
          </button>
        </form>
        <p class="rodape-form">
          Não tem conta?
          <a href="/cadastro">
            Cadastre-se
          </a>
          .
        </p>
      </section>
    </main>
  </body>
</html>
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1" name="viewport"/>
    <title>
      Criar conta | Beleza que faz bem
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
          CADASTRO
        </span>
        <h1>
          Criar conta
        </h1>
        <p>
          Contas cadastradas aqui recebem o perfil de cliente.
        </p>
        % if mensagem:
        <p class="alerta" role="alert">
          {{mensagem}}
        </p>
        % end
        <form action="/cadastro" class="form-vertical" method="post">
          <input name="csrf" type="hidden" value="{{csrf}}"/>
          <label>
            Nome completo
            <input maxlength="80" minlength="2" name="nome" required=""/>
          </label>
          <label>
            E-mail
            <input autocomplete="username" name="email" required="" type="email"/>
          </label>
          <label>
            Senha (mínimo 10 caracteres)
            <input autocomplete="new-password" minlength="10" name="senha" required="" type="password"/>
          </label>
          <label>
            Confirmar senha
            <input autocomplete="new-password" minlength="10" name="confirmacao" required="" type="password"/>
          </label>
          <button class="botao" type="submit">
            Criar conta
          </button>
        </form>
        <p class="rodape-form">
          Já tem conta?
          <a href="/login">
            Entrar
          </a>
          .
        </p>
      </section>
    </main>
  </body>
</html>
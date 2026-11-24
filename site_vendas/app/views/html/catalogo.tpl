<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Catálogo | Beleza que faz bem</title><link rel="stylesheet" href="/static/css/nivel3.css"><script defer src="/static/js/catalogo.js"></script></head><body class="pagina-interna">
<header class="topo-site"><a class="marca" href="/inicio">Beleza que faz bem</a><nav class="menu-principal"><a href="/inicio">Início</a>
% if usuario:
<a href="/conta">Minha conta</a>
% if usuario.papel == 'gerente':
<a href="/produtos">Gerenciar</a>
% end
<form class="inline-form" method="post" action="/logout"><input name="csrf" type="hidden" value="{{csrf}}"><button class="btn-discreto">Sair</button></form>
% else:
<a href="/login">Entrar</a><a href="/cadastro" class="btn-nav">Criar conta</a>
% end
</nav></header>
<main class="container"><div class="titulo-pagina"><span class="sobrelinha">NOSSA SELEÇÃO</span><h1>Catálogo de produtos</h1><p>Consulte os itens disponíveis. O gerenciamento é exclusivo da equipe.</p></div>
<label class="sr-only" for="busca">Pesquisar catálogo</label><input class="campo-busca" type="search" id="busca" placeholder="Buscar pelo nome ou categoria">
% if not produtos:
<section class="painel"><p>Nenhum produto cadastrado no momento.</p></section>
% else:
<div class="grade-produtos" id="grade">
% for produto in produtos:
<article class="cartao-produto" data-busca="{{(produto.nome + ' ' + produto.categoria).casefold()}}"><div class="cartao-cabecalho"><span class="categoria">{{produto.categoria}}</span><span class="situacao {{'disponivel' if produto.estoque > 0 else 'esgotado'}}">{{'Disponível' if produto.estoque > 0 else 'Esgotado'}}</span></div><h2>{{produto.nome}}</h2><p class="preco">R$ {{f'{produto.preco:.2f}'.replace('.', ',')}}</p><p class="estoque">{{produto.estoque}} unidade(s) em estoque</p></article>
% end
</div><p id="sem-resultados" hidden>Nenhum produto corresponde à pesquisa.</p>
% end
</main></body></html>

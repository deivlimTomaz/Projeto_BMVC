<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Beleza que faz bem | Início</title>
<link rel="stylesheet" href="/static/css/inicio.css"><link rel="stylesheet" href="/static/css/nivel3.css">
<script defer src="/static/js/inicio.js"></script></head>
<body>
<header class="topo-site"><a href="/inicio" class="marca">Beleza que faz bem</a>
<nav class="menu-principal"><a href="/catalogo">Catálogo</a>
% if usuario:
 <a href="/conta">Minha conta</a>
 % if usuario.papel == 'gerente':
 <a href="/produtos">Gerenciar produtos</a>
 % end
 <form action="/logout" method="post" class="inline-form"><input type="hidden" name="csrf" value="{{csrf}}"><button class="btn-discreto" type="submit">Sair</button></form>
% else:
 <a href="/login">Entrar</a><a class="btn-nav" href="/cadastro">Criar conta</a>
% end
</nav></header>
<div class="logos"><img class="anim-item" src="/static/img/natura-logo-png_seeklogo-451985.png" alt="Logo Natura"><span class="logos-divisor"></span><img class="anim-item" src="/static/img/logotipo.png" alt="Logo da loja"></div>
<div class="chamada-usuario anim-item">
% if usuario:
 <p>Olá, {{usuario.nome}}.</p><a href="/conta">Ver minha conta</a>
% else:
 <p>Encontre seus produtos e tenha uma conta para acompanhar seu cadastro.</p>
 <div class="acoes-inicio"><a class="botao" href="/cadastro">Criar conta</a><a class="botao botao-claro" href="/login">Fazer login</a></div>
% end
</div>
<section class="destaque"><img class="anim-item" src="/static/img/naturafoto1.png" alt="Produtos de beleza e bem-estar"><div class="apresentacao-texto anim-item"><h2>Beleza que faz bem</h2><p>Conheça os produtos de cuidados com a pele, perfumaria e maquiagem disponíveis em nosso catálogo.</p><a href="/catalogo" class="botao">Explorar catálogo</a></div></section>
</body></html>
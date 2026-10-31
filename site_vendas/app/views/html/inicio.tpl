<!DOCTYPE html>
<html lang="pt-BR">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>Deuza Pereira - NATURA</title>
   <link rel="stylesheet" type="text/css" href="/static/css/inicio.css">
   <script src="/static/js/inicio.js"></script>

</head>
<body>
   <div class="logos">
      <img class="anim-item" src="/static/img/natura-logo-png_seeklogo-451985.png" alt="Natura logo">
      <span class="logos-divisor anim-item"></span>
      <img class="anim-item" src="/static/img/logotipo.png" alt="Minha logo">
   </div>

   <!-- <h1 style="text-align:center;">Minha página NATURA :)</h1> -->

   <form class="search-box" action="/search" method="GET">
      <img class="lupa" src="/static/img/lupa.png" alt="Lupa logo">

      <input type="text" name="q" placeholder="Buscar produtos..." autocomplete="off">

      <button type="submit">Buscar</button>
   </form>

   <section class="destaque">
      <img class="anim-item" src="/static/img/naturafoto1.png" alt="Duas mulheres sorrindo">
      <div class="apresentacao-texto anim-item">
         <h2>Beleza que faz bem</h2>
         <p>
            Conheça os produtos de cuidados com a pele, perfumaria e maquiagem feitos para valorizar o que há
            de mais bonito em você.
         </p>

         <a href="/produtos" class="botao">Conheça os produtos</a>
      </div>
   </section>
</body>
</html>

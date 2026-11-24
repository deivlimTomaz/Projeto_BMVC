document.addEventListener('DOMContentLoaded', () => {
  const busca = document.querySelector('#busca');
  const cartoes = [...document.querySelectorAll('.cartao-produto')];
  const aviso = document.querySelector('#sem-resultados');
  if (!busca) return;
  busca.addEventListener('input', () => {
    const termo = busca.value.trim().toLocaleLowerCase('pt-BR');
    let visiveis = 0;
    for (const cartao of cartoes) {
      const mostra = cartao.dataset.busca.includes(termo);
      cartao.hidden = !mostra;
      if (mostra) visiveis++;
    }
    if (aviso) aviso.hidden = visiveis !== 0;
  });
});

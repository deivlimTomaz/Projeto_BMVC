document.addEventListener('DOMContentLoaded', () => {
  const busca = document.querySelector('#buscar-produto');
  const linhas = [...document.querySelectorAll('.linha-produto')];
  const aviso = document.querySelector('#sem-resultados');
  if (busca) busca.addEventListener('input', () => {
    const termo = busca.value.trim().toLocaleLowerCase('pt-BR');
    let visiveis = 0;
    for (const linha of linhas) {
      const mostra = linha.dataset.nome.includes(termo) || linha.dataset.categoria.includes(termo);
      linha.hidden = !mostra;
      if (mostra) visiveis++;
    }
    if (aviso) aviso.hidden = visiveis !== 0;
  });
  for (const formulario of document.querySelectorAll('.form-excluir')) {
    formulario.addEventListener('submit', evento => {
      if (!window.confirm(`Excluir o produto "${formulario.dataset.nome}"?`)) evento.preventDefault();
    });
  }
});
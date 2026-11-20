
document.addEventListener("DOMContentLoaded", () => {

    const campoBusca = document.getElementById("buscar-produto");
    const linhas = document.querySelectorAll(".linha-produto");
    const mensagemBusca = document.getElementById("sem-resultados");

    // Filtra produtos pelo nome ou categoria
    if (campoBusca) {
        campoBusca.addEventListener("input", () => {
            const termo = campoBusca.value.trim().toLowerCase();
            let encontrados = 0;

            linhas.forEach(linha => {
                const nome = linha.dataset.nome;
                const categoria = linha.dataset.categoria;

                const corresponde =
                    nome.includes(termo) ||
                    categoria.includes(termo);

                linha.hidden = !corresponde;

                if (corresponde) {
                    encontrados++;
                }
            });

            if (mensagemBusca) {
                mensagemBusca.hidden = encontrados > 0;
            }
        });
    }

    // Confirma a exclusão antes de enviar o formulário
    const formulariosExclusao =
        document.querySelectorAll(".form-excluir");

    formulariosExclusao.forEach(formulario => {
        formulario.addEventListener("submit", evento => {
            const nome = formulario.dataset.nome;

            const confirmado = window.confirm(
                `Deseja realmente excluir o produto "${nome}"?`
            );

            if (!confirmado) {
                evento.preventDefault();
            }
        });
    });

});

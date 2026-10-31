document.addEventListener("DOMContentLoaded", function (event) {
    
    const itens = document.querySelectorAll('.anim-item');

    itens.forEach((item, indice) => {
        setTimeout(() => {
            item.classList.add('visivel');
        }, indice * 300);
    });
});


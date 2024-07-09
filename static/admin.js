const linhas = document.querySelectorAll('.linha');
const detalhes = document.querySelectorAll('.mais')

let id_produto = NaN
function clicou(linha) {
    // muda o estilo da linha selecionada
    linhas.forEach(element => {
        element.classList.remove('selecionado');
    });

    let selecionado = document.getElementById(linha);
    let mostrar = document.getElementById('produto-'+linha);

    console.log(mostrar);
    mostrar.classList.add('ativo');
    selecionado.classList.add('selecionado');
};

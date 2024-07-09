const imagem = document.getElementById('img');
const previw = document.getElementById('previw');

imagem.addEventListener("change", () => {
    if(imagem.files) {
        const img = imagem.files[0];
        console.log(img)
        if(img['size'] < 2097152) {
            const leitor = new FileReader();

            console.log(img['size'])

            leitor.onload = () => {
                previw.src = leitor.result;
            }
            
            leitor.readAsDataURL(img)
        } else {
            alert('Erro! \nArquivo muito grande. Maximo suportado 2MB.')
        }
    }
});

previw.addEventListener('click', () => {
    imagem.click()
})

const nova_imagem = document.getElementById('nova-img');
const novo_previw = document.getElementById('edit-previw');

nova_imagem.addEventListener('change', (e) => {
    if(nova_imagem.files) {
        const n_img = nova_imagem.files[0];
        console.log(n_img)
        if(n_img['size'] < 2097152) {
            const n_leitor = new FileReader();

            console.log(n_img['size'])

            n_leitor.onload = () => {
                previw.src = n_leitor.result;
            }
            
            n_leitor.readAsDataURL(img)
        } else {
            alert('Erro! \nArquivo muito grande. Maximo suportado 2MB.')
        }
    }
});

novo_previw.addEventListener('click', () => {
    nova_imagem.click()
})
const hamburger = document.querySelector(".hamburguer");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
})
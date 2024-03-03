const hamburger = document.querySelector(".hamburguer");
const navMenu = document.querySelector(".nav-menu");

hamburger.addEventListener("click", () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
})

var item = document.querySelectorAll("[data-anima]")

function animeScroll() {
    let windowTop = window.pageYOffset + window.innerHeight * 1

    item.forEach((element) => {
        if(windowTop > element.offsetTop) {
            element.classList.add("animate")
        } else {
            element.classList.remove("animate")
        }
    })
}

animeScroll()

window.addEventListener("scroll", function() {
    animeScroll()
})
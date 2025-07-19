(function () {
    window.onload = function () {
        const preloader = document.querySelector('.page-loading');
        preloader.classList.remove('active');
        setTimeout(function () {
            preloader.remove();
        }, 1000);
    };
})();


document.addEventListener("DOMContentLoaded", function () {
    new Typed('#typed-output', {
        strings: ["ventas.", "inventario.", "finanzas (chatbot)."],
        typeSpeed: 90,
        backSpeed: 30,
        backDelay: 1000,
        loop: true,
        showCursor: false
    });
});


document.addEventListener("DOMContentLoaded", function () {
    const dropdownToggles = document.querySelectorAll(".nav-item.dropdown > .nav-link");

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener("click", function (e) {
            e.preventDefault();
            const submenu = toggle.nextElementSibling;
            document.querySelectorAll(".dropdown-menu.show").forEach(function (menu) {
                if (menu !== submenu) menu.classList.remove("show");
            });
            submenu.classList.toggle("show");
        });
    });
});


document.getElementById("year").textContent = new Date().getFullYear();

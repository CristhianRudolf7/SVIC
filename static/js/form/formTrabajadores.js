<<<<<<< HEAD
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".input-group-text").forEach(function (toggle) {
        toggle.addEventListener("click", function () {
            const input = this.previousElementSibling;
            const isPassword = input.type === "password";
            input.type = isPassword ? "text" : "password";
            this.setAttribute("data-password", !isPassword);
            this.querySelector(".password-eye").classList.toggle("show-password", !isPassword);
        });
    });
});
=======
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".input-group-text").forEach(function (toggle) {
      toggle.addEventListener("click", function () {
        const input = this.previousElementSibling;
        const isPassword = input.type === "password";
        input.type = isPassword ? "text" : "password";
        this.setAttribute("data-password", !isPassword);
        this.querySelector(".password-eye").classList.toggle("show-password", !isPassword);
      });
    });
  });
>>>>>>> MVP

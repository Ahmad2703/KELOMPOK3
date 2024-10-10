//Validasi Login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');

    loginForm.addEventListener('submit', (event) => {
        const username = usernameInput.value.trim();
        const password = passwordInput.value.trim();

        // Validasi ketika username dan password harus terisi
        if (username === "" || password === "") {
            event.preventDefault();
            alert("Username dan password harus diisi!");
            return;
        }

        // Validasi untuk panjang password
        if (password.length < 6) {
            event.preventDefault();
            alert("Password harus memiliki setidaknya 6 karakter.");
            return;
        }

        // Jika validasi berhasil, form akan dikirim
        alert("Login berhasil!");
    });
});

//Js Hamburger Sidebar
const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});



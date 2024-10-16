// Validasi Login
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('form');
    const loginUsernameInput = document.getElementById('loginusername');
    const loginPasswordInput = document.getElementById('loginpassword');

    // Tambahkan event listener untuk form login
    loginForm.addEventListener('submit', (event) => {
        const username = loginUsernameInput.value.trim();
        const password = loginPasswordInput.value.trim();

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

        // Jika validasi berhasil
        alert("Login berhasil!");
    });

    // Validasi Signup
    const signupForm = document.getElementById('signupForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');

    // Tambahkan event listener untuk form signup
    signupForm.addEventListener('submit', (event) => {
        const username = usernameInput.value.trim();
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        // Validasi ketika semua field harus terisi
        if (username === "" || email === "" || password === "") {
            event.preventDefault();
            alert("Semua field harus diisi!");
            return;
        }

        // Validasi untuk format email
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (!emailPattern.test(email)) {
            event.preventDefault();
            alert("Email tidak valid!");
            return;
        }

        // Validasi untuk panjang password
        if (password.length < 6) {
            event.preventDefault();
            alert("Password harus memiliki setidaknya 6 karakter.");
            return;
        }

        // Jika validasi berhasil
        alert("Signup berhasil! Silahkan login kembali.");
    });
});

//Js Hamburger Sidebar
const hamBurger = document.querySelector(".toggle-btn");

hamBurger.addEventListener("click", function () {
    document.querySelector("#sidebar").classList.toggle("expand");
});

// Validasi Logout
document.getElementById('LogOutButton').addEventListener('click', function () {
    // Tampilkan dialog konfirmasi
    const confirmation = confirm("Apakah Anda yakin ingin logout?");

    if (confirmation) {
        // Jika pengguna memilih "OK", lanjutkan proses logout
        alert("Anda telah logout.");
        window.location.href = 'home.html';
    } else {
        // Jika pengguna memilih "Cancel"
        alert("Logout dibatalkan.");
    }
});

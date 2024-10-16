
// Validasi signUp
$(document).ready(function () {
    const $signupForm = $('#signupForm');
    const $usernameInput = $('#username');
    const $emailInput = $('#email');
    const $passwordInput = $('#password');

    // Tambahkan event listener untuk form signup
    $signupForm.on('submit', function (event) {
        const username = $usernameInput.val().trim();
        const email = $emailInput.val().trim();
        const password = $passwordInput.val().trim();

        console.log("Username:", username); // Debugging
        console.log("Email:", email); // Debugging
        console.log("Password:", password); // Debugging

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

// Validasi Login
$(document).ready(function () {
    const $loginForm = $('form');
    const $loginUsernameInput = $('#loginusername');
    const $loginPasswordInput = $('#loginpassword');

    // Tambahkan event listener untuk form login
    $loginForm.on('submit', function (event) {
        const username = $loginUsernameInput.val().trim();
        const password = $loginPasswordInput.val().trim();

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
});

// Buka-tutup Sidebar
$(document).ready(function () {
    // Toggle sidebar
    $(".toggle-btn").click(function () {
        $("#sidebar").toggleClass("expand");
    });

    // Toggle dropdown menu  "Class"
    $(".has-dropdown").click(function (e) {
        e.preventDefault();
        $(this).next(".sidebar-dropdown").slideToggle(300);
    });
});

// Profile
$(document).ready(function () {
    // Klik untuk image upload
    $('#profileImage').on('click', function () {
        $('#imageUpload').click();
    });

    // Mengubah gambar profil saat user memilih gambar baru
    $('#imageUpload').on('change', function (event) {
        const image = event.target.files[0];
        if (image) {
            const reader = new FileReader();
            reader.onload = function (e) {
                $('#profileImage').attr('src', e.target.result);
            };
            reader.readAsDataURL(image);
        }
    });

});

// Fungsi jQuery untuk menampilkan animasi eksternal 
$(window).on('load', function () {
    // Atur delay selama 2 detik sebelum preloader dihilangkan
    setTimeout(function () {
        // Hilangkan animasi
        $('.preloader').fadeOut('slow', function () {
             // Tampilkan konten setelah preloader dihilangkan supaya lebih halus
            $('.content').fadeIn('slow');
        });
    }, 2000); // 2000ms = 2 detik
});

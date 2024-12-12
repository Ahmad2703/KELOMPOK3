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
        // alert("Login berhasil!");
    });
});

// Validasi Logout
$('#LogOutButton').on('click', function () {
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

// Fungsi jQuery untuk menampilkan animasi
$(document).ready(function () {
    // Tambahkan delay selama 1 detik (1000 milidetik)
    setTimeout(function () {
        // Menghilangkan elemen preloader setelah 1 detik
        $('.preloader').fadeOut('slow');
    }, 1000); // 1000 milidetik = 1 detik
});


// Fungsi jQuery untuk menampilkan kalender
$(document).ready(function () {
    const today = new Date();
    let currentMonth = today.getMonth();
    let currentYear = today.getFullYear();

    const months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];

    function renderCalendar(month, year) {
        const firstDay = new Date(year, month).getDay();
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        $("#currentMonth").text(`${months[month]} ${year}`);

        let calendarBody = $("#calendarBody");
        calendarBody.empty();

        let date = 1;
        for (let i = 0; i < 6; i++) {
            let row = $("<tr></tr>");
            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDay) {
                    row.append("<td></td>");
                } else if (date > daysInMonth) {
                    break;
                } else {
                    let cell = $("<td></td>").text(date);
                    if (date === today.getDate() && year === today.getFullYear() && month === today.getMonth()) {
                        cell.addClass("current-day");
                    }
                    row.append(cell);
                    date++;
                }
            }
            calendarBody.append(row);
        }
    }

    $("#prevMonth").click(function () {
        currentMonth--;
        if (currentMonth < 0) {
            currentMonth = 11;
            currentYear--;
        }
        renderCalendar(currentMonth, currentYear);
    });

    $("#nextMonth").click(function () {
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        renderCalendar(currentMonth, currentYear);
    });

    renderCalendar(currentMonth, currentYear);
});
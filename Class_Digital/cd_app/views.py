from django.shortcuts import render, redirect
from cd_app.forms import SignupForm, UserProfileInfoForm, UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, path
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course
from datetime import datetime, timedelta, date
from calendar import monthrange

@login_required
def dashboard(request):
    courses = Course.objects.all()
    return render(request, 'cd_app/dashboard.html', {'courses': courses})

def home(request):
    return render(request, 'cd_app/home.html')

def forum_view(request):
    courses = Course.objects.all()
    return render(request, 'cd_app/forum.html', {'courses': courses})

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def signup_view(request):
    if request.method == 'POST':
        # Inisialisasi kedua form
        user_form = SignupForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        # Validasi form
        if user_form.is_valid() and profile_form.is_valid():
            # Simpan data User
            try:
                # Simpan user ke database (tapi belum langsung commit ke DB)
                user = user_form.save(commit=False)
                user.set_password(user_form.cleaned_data['password'])  # Enkripsi password
                user.save()  # Simpan user ke database

                # Simpan data UserProfileInfo
                profile = profile_form.save(commit=False)
                profile.user = user  # Hubungkan dengan User yang baru dibuat
                profile.save()

                # Tampilkan pesan sukses dan redirect ke halaman login
                messages.success(request, "Akun berhasil dibuat. Silakan login.")
                return redirect('cd_app:login')
            except Exception as e:
                messages.error(request, f"Terjadi kesalahan: {e}")
                return redirect('cd_app:signup')
        else:
            # Tampilkan pesan error jika form tidak valid
            messages.error(request, "Form tidak valid. Mohon cek kembali data yang dimasukkan.")
    else:
        # Jika GET, tampilkan form kosong
        user_form = SignupForm()
        profile_form = UserProfileInfoForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'cd_app/signup.html', context)

def login_view(request):
    # Jika user sudah login, redirect ke dashboard
    if request.user.is_authenticated:
        return redirect('cd_app:dashboard')  # Ganti dengan nama URL setelah login

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Melakukan autentikasi
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Jika autentikasi berhasil, login pengguna
            login(request, user)
            return redirect('cd_app:dashboard')  # Ganti dengan nama URL setelah login
        else:
            # Jika autentikasi gagal
            messages.error(request, 'Username atau password salah.')
            return render(request, 'cd_app/login.html')
    
    # Render form login jika GET
    return render(request, 'cd_app/login.html')

@login_required
def edit_profile(request):
    try:
        profile = request.user.profile
    except UserProfileInfo.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileInfoForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_success')  # Ubah sesuai dengan URL sukses yang Anda inginkan
    else:
        form = UserProfileInfoForm(instance=profile)

    return render(request, 'cd_app/profile.html', {'form': form})

def calendar_view(request):
    # Mendapatkan bulan dan tahun saat ini
    today = date.today()
    current_month = today.month
    current_year = today.year

    month = int(request.GET.get('month', current_month))
    year = int(request.GET.get('year', current_year))

    # Mendapatkan jumlah hari dalam bulan
    num_days = monthrange(year, month)[1]
    first_day_of_month = date(year, month, 1).weekday()

    # Membuat struktur kalender
    calendar_data = []
    current_day = 1

    # Baris pertama kalender (padding untuk hari sebelum tanggal 1)
    row = [''] * first_day_of_month
    while len(row) < 7:
        row.append(current_day)
        current_day += 1
    calendar_data.append(row)

    # Baris-baris berikutnya
    while current_day <= num_days:
        row = []
        for _ in range(7):
            if current_day <= num_days:
                row.append(current_day)
                current_day += 1
            else:
                row.append('')  # Padding untuk hari setelah akhir bulan
        calendar_data.append(row)

    # Data untuk template
    context = {
        'calendar_data': calendar_data,
        'month': month,
        'year': year,
        'month_name': datetime(year, month, 1).strftime('%B'),
        'today': today.day,  # Tanggal hari ini
        'current_month': current_month,
        'current_year': current_year,
    }

    return render(request, 'cd_app/calendar.html', context)
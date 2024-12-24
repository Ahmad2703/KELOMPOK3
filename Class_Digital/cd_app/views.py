from django.shortcuts import render, redirect, get_object_or_404
from cd_app.forms import SignupForm, UserProfileInfoForm, UserProfileInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse, path
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Presence, UserProfileInfo, Comment
from datetime import datetime, timedelta, date
from calendar import monthrange
from django.utils import timezone
from .forms import CommentForm

@login_required
def dashboard(request):
    # Ambil semua mata kuliah yang diambil oleh student
    if request.user.profile.role == 'student':
        courses = request.user.profile.courses.all()  # Mata kuliah yang diambil oleh student
    else:
        # Untuk teacher, ambil mata kuliah yang diajarkan oleh teacher
        courses = Course.objects.filter(teacher=request.user.profile)

    return render(request, 'cd_app/dashboard.html', {'courses': courses})

def home(request):
    return render(request, 'cd_app/home.html')

def setting_view(request):
    return render(request, 'cd_app/setting.html')

@login_required
def forum_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    comments = Comment.objects.filter(course=course).order_by('-created_at')
    
    # Pastikan user saat ini adalah teacher dari course
    is_teacher = request.user == course.teacher.user

    if request.method == 'POST':
        # Tangani form pengumuman
        if 'announcement' in request.POST and is_teacher:
            announcement = request.POST.get('announcement')
            course.announcement = announcement
            course.save()
            return redirect('cd_app:forum', course_id=course.id)

        # Tangani form komentar
        elif 'delete_comment' in request.POST:
            comment_id = request.POST.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)

            # Pastikan mengambil UserProfileInfo
            user_profile = UserProfileInfo.objects.get(user=request.user)

            # Pastikan hanya pemilik komentar atau admin yang dapat menghapus
            if comment.user != user_profile and not request.user.is_staff:
                return HttpResponseForbidden("Anda tidak memiliki izin untuk menghapus komentar ini.")

            comment.delete()
            return redirect('cd_app:forum', course_id=course.id)
        
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                user_profile = UserProfileInfo.objects.get(user=request.user)
                comment.user = user_profile
                comment.course = course
                comment.save()
                return redirect('cd_app:forum', course_id=course.id)
    else:
        form = CommentForm()

    return render(request, 'cd_app/forum.html', {
        'course': course,
        'comments': comments,
        'form': form,
        'is_teacher': is_teacher,  # Berikan informasi apakah user adalah teacher
    })

@login_required
def task_view(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_teacher = request.user.profile.role == 'teacher'

    if request.method == 'POST' and is_teacher:
        # Proses upload materi PDF
        pdf_material = request.FILES.get('pdf_material')
        if pdf_material:
            course.pdf_material = pdf_material

        # Proses upload URL video YouTube
        video_url = request.POST.get('video_url')
        if video_url:
            course.video_url = video_url
        
        course.save()
        return redirect('cd_app:task', course_id=course.id)

    return render(request, 'cd_app/task.html', {'course': course, 'is_teacher': is_teacher})


@login_required
def presence_view(request, course_id):
    try:
        # Ambil course dan profile pengguna
        course = Course.objects.get(id=course_id)
        user_profile = UserProfileInfo.objects.get(user=request.user)  # Ambil UserProfileInfo
    except Course.DoesNotExist:
        return redirect('error_page')  # Halaman error jika course tidak ditemukan
    except UserProfileInfo.DoesNotExist:
        return redirect('profile_create')  # Halaman untuk membuat profil jika belum ada

    # Tentukan tanggal presensi untuk minggu tertentu
    presence_dates = {
        1: timezone.make_aware(timezone.datetime(2024, 12, 16, 20, 0, 0)),
        2: timezone.make_aware(timezone.datetime(2024, 12, 20, 20, 0, 0)),
        3: timezone.make_aware(timezone.datetime(2024, 12, 26, 20, 0, 0)),
        4: timezone.make_aware(timezone.datetime(2024, 12, 2, 20, 0, 0)),
    }

    # Ambil semua presensi untuk course ini dan user ini
    presences = Presence.objects.filter(user=user_profile, course=course)

    # Persiapkan data untuk ditampilkan ke template
    presence_data = {}
    for week, date in presence_dates.items():
        # Cari status presensi untuk minggu ini
        presence = presences.filter(week=week).first()
        if presence:
            status = presence.status
        else:
            status = 'Belum Presensi'

        # Tambahkan data presensi ke dictionary
        presence_data[week] = {
            'date': date,
            'status': status
        }

    # Kirim data ke template
    context = {
        'course': course,
        'presence_dates': presence_data.items()  # Mengubahnya menjadi items agar bisa diiterasi di template
    }
    return render(request, 'cd_app/presence.html', context)

def recap_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return render(request, '404.html')
    
    return render(request, 'cd_app/recap_values.html', {'course': course})

def list_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)  # Mendapatkan kursus berdasarkan ID
    except Course.DoesNotExist:
        return render(request, '404.html')  # Jika kursus tidak ditemukan
    
    # Mengambil semua mahasiswa yang terdaftar di kursus ini
    enrolled_users = course.enrolled_users.all()  # Relasi Many-to-Many
    
    return render(request, 'cd_app/list_mahasiswa.html', {
        'course': course,
        'enrolled_users': enrolled_users
    })

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
        # Mengambil profil pengguna yang sedang login
        profile = request.user.profile
    except UserProfileInfo.DoesNotExist:
        # Jika profil tidak ada, buat profil baru
        profile = None

    if request.method == 'POST':
        # Form untuk mengedit data pengguna dan profil pengguna
        user_form = UserProfileInfoForm(request.POST, instance=request.user)
        profile_form = UserProfileInfoForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Simpan perubahan pada kedua form
            user_form.save()  # Mengubah data user (nama, email)
            profile_form.save()  # Mengubah data profil (telepon, about, gambar)

    else:
        # Jika metode GET, gunakan form dengan data pengguna yang ada
        user_form = UserProfileInfoForm(instance=request.user)
        profile_form = UserProfileInfoForm(instance=profile)

    return render(request, 'cd_app/profile.html', {'user_form': user_form, 'profile_form': profile_form})

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
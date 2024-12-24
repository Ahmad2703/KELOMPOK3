from django.contrib.auth.models import User
from django.db import models

class UserProfileInfo(models.Model):
    # Relasi One-to-One ke User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Informasi tambahan
    image = models.ImageField(upload_to='profile_pics', blank=True)
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    about = models.TextField(blank=True)

    # Role: 'student' atau 'teacher'
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # Relasi Many-to-Many untuk siswa yang mendaftar course
    courses = models.ManyToManyField('Course', related_name='enrolled_users', blank=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Course(models.Model):
    # Informasi course
    name = models.CharField(max_length=200)
    schedule = models.CharField(max_length=100)
    url = models.URLField()
    video_url = models.URLField(blank=True, null=True, help_text="URL video pembelajaran (contoh: YouTube)")
    pdf_material = models.FileField(upload_to='materials/', blank=True, null=True, help_text="Unggah materi dalam format PDF")
    announcement = models.TextField(blank=True, null=True)

    # Relasi ke teacher (One-to-Many)
    teacher = models.ForeignKey(
        UserProfileInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teaching_courses',
        limit_choices_to={'role': 'teacher'},  # Hanya user dengan role 'teacher'
    )

    def __str__(self):
        return self.name

class Presence(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    week = models.IntegerField()
    status = models.CharField(max_length=50, choices=[('Belum Presensi', 'Belum Presensi'), ('Presensi telah dilakukan', 'Presensi telah dilakukan')])
    date = models.DateTimeField(null=True, blank=True)  # Pastikan 'null=True' jika belum ada tanggal presensi

    def __str__(self):
        return f"Presensi {self.user.username} - Minggu {self.week}"
    
class Comment(models.Model):
    user = models.ForeignKey(UserProfileInfo, on_delete=models.CASCADE)  # Menghubungkan ke UserProfileInfo
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Menghubungkan ke kursus
    content = models.TextField()  # Isi komentar
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu komentar dibuat

    def __str__(self):
        return f"Comment by {self.user.user.username} on {self.course.title}"
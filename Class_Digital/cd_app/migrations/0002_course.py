# Generated by Django 5.1.3 on 2024-11-21 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cd_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('teacher', models.CharField(max_length=100)),
                ('schedule', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='img/')),
                ('url', models.URLField()),
            ],
        ),
    ]

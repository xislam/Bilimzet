# Generated by Django 4.2.15 on 2024-08-25 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='Имя')),
                ('phone_number', models.CharField(error_messages={'unique': 'Пользователь с указанным номером телефона уже существует.'}, max_length=18, unique=True, verbose_name='Телефон')),
                ('device_token', models.CharField(blank=True, max_length=500, null=True, verbose_name='Токен устройства')),
                ('phone_number_verified', models.BooleanField(default=False, verbose_name='Верифицирован')),
                ('verification_code', models.CharField(blank=True, max_length=6, null=True)),
                ('receive_notifications', models.BooleanField(blank=True, default=True, verbose_name='Получать уведомления')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/')),
                ('receive_promotions', models.BooleanField(blank=True, default=True, verbose_name='Получать акции')),
                ('receive_email_notifications', models.BooleanField(blank=True, default=True, verbose_name='Получать уведомления по почте')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]

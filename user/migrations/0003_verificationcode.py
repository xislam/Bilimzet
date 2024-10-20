# Generated by Django 4.2.15 on 2024-09-02 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_email_alter_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='code', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

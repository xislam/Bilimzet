# Generated by Django 4.2.15 on 2024-10-28 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_certificate_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='certificates'),
        ),
    ]
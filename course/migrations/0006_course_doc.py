# Generated by Django 4.2.15 on 2024-11-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_remove_userprogress_progress_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='doc',
            field=models.FileField(blank=True, null=True, upload_to='doc_curs', verbose_name='Информация о курсе виде файла'),
        ),
    ]

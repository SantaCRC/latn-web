# Generated by Django 4.2.6 on 2024-03-17 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_document_profile_delete_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='key_url',
        ),
        migrations.AddField(
            model_name='profile',
            name='key',
            field=models.FileField(blank=True, null=True, upload_to='keys/'),
        ),
    ]
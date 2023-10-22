# Generated by Django 4.0 on 2023-01-09 05:51

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_message_to_group_remove_message_to_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(upload_to='uploads/')),
                ('image', models.ImageField(default='default.jpg', upload_to=accounts.models.get_image_path)),
            ],
        ),
    ]
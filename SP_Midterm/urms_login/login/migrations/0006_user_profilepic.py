# Generated by Django 5.1.7 on 2025-03-09 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_alter_user_userid'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilePic',
            field=models.ImageField(default='profile_pictures/default.png', upload_to='profile_pictures/'),
        ),
    ]

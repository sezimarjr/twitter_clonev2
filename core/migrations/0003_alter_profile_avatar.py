# Generated by Django 5.1.3 on 2024-11-26 17:55

import core.models.profile
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='images/user_placeholder.png', upload_to='avatar', validators=[core.models.profile.validate_image]),
        ),
    ]
# Generated by Django 3.1 on 2021-11-16 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_post_ikes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='ikes',
            new_name='likes',
        ),
    ]
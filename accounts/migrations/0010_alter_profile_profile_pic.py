# Generated by Django 4.2.7 on 2023-12-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='/images/default.png', null=True, upload_to='images/'),
        ),
    ]

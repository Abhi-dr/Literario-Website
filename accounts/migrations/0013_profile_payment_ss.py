# Generated by Django 4.2.7 on 2023-12-29 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_profile_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='payment_ss',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-12-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_registration_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='approved_by_head',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 4.0.4 on 2023-06-20 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True},
        ),
    ]
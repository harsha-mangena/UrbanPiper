# Generated by Django 4.1.2 on 2022-10-25 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodordering', '0005_alter_store_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='Address',
            new_name='Store_Address',
        ),
    ]

# Generated by Django 4.1.2 on 2022-10-26 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodordering', '0011_item_created_at_store_created_at_user_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]

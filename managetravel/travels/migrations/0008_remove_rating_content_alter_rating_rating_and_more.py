# Generated by Django 4.2.7 on 2024-01-31 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0007_remove_users_roles_roles_remove_users_roles_users_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='content',
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.SmallIntegerField(),
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]

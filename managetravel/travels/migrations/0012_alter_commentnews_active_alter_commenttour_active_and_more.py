# Generated by Django 4.2.7 on 2024-02-02 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0011_alter_commentnews_active_alter_commenttour_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentnews',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='commenttour',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]

# Generated by Django 4.2.7 on 2024-02-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0016_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together={('user', 'news')},
        ),
    ]

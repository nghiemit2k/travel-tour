# Generated by Django 4.2.7 on 2024-02-03 12:53

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0012_alter_commentnews_active_alter_commenttour_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('content', ckeditor.fields.RichTextField()),
                ('news', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travels.news')),
                ('tour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='travels.tours')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='commenttour',
            name='tour',
        ),
        migrations.RemoveField(
            model_name='commenttour',
            name='user',
        ),
        migrations.DeleteModel(
            name='CommentNews',
        ),
        migrations.DeleteModel(
            name='CommentTour',
        ),
    ]

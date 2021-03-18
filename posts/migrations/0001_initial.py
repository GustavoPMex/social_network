# Generated by Django 3.1.7 on 2021-03-18 01:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PostUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_user', models.TextField()),
                ('date_post', models.DateTimeField(auto_now_add=True)),
                ('like_post', models.DecimalField(decimal_places=0, max_digits=100)),
                ('dislike_post', models.DecimalField(decimal_places=0, max_digits=100)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
                'ordering': ['date_post'],
            },
        ),
    ]
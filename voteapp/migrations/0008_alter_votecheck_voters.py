# Generated by Django 4.0 on 2023-08-26 15:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('voteapp', '0007_alter_votecheck_voters'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votecheck',
            name='voters',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]

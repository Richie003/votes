# Generated by Django 4.0 on 2023-08-27 08:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0008_alter_votecheck_voters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='votetable',
            name='candidates',
        ),
        migrations.AddField(
            model_name='votetable',
            name='candidates',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='voteapp.candidate'),
            preserve_default=False,
        ),
    ]

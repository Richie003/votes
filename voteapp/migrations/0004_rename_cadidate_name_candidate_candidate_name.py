# Generated by Django 4.0 on 2023-08-24 08:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0003_candidate_display_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='cadidate_name',
            new_name='candidate_name',
        ),
    ]
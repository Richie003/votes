# Generated by Django 4.0 on 2023-08-24 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voteapp', '0002_candidate_added_alter_votetable_candidates'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='display_image',
            field=models.ImageField(blank=True, upload_to='candidates/'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-29 12:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_remove_gig_genre_gig_genres_alter_application_client_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='musician',
            name='rating',
        ),
    ]

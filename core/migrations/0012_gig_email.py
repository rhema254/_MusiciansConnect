# Generated by Django 5.0.1 on 2024-02-16 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_gig_dry_run_alter_gig_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='email',
            field=models.EmailField(default='myemailgmail.com', max_length=254),
            preserve_default=False,
        ),
    ]

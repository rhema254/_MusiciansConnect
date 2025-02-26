# Generated by Django 5.0.1 on 2024-03-25 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0079_alter_musician_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='Profession_category',
            field=models.CharField(choices=[('', 'Select one'), ('Singer', 'Singer'), ('Songwriter', 'Songwriter'), ('Producer', 'Producer'), ('Vocalist', 'Vocalist'), ('Band', 'Band'), ('Instrumentalist', 'Instrumentalist'), ('Sound-engineer', 'Sound Engineer'), ('Music-educator', 'Music Educator'), ('Folk-traditional', 'Folk and Traditional'), ('DJ', 'DJ'), ('Cover-band', 'Cover Band')], max_length=25, null=True),
        ),
    ]

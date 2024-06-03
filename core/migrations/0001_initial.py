# Generated by Django 4.2.5 on 2024-02-06 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='musicians',
            fields=[
                ('musicians_id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('musicians_phone_no', models.CharField(blank=True, max_length=50, null=True)),
                ('musician_email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=50)),
                ('rating', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('username', models.CharField(max_length=50)),
                ('skill_level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')], max_length=20)),
                ('genre', models.CharField(choices=[('Soul', 'Soul'), ('Jazz', 'Jazz'), ('Benga', 'Benga'), ('Pop', 'Pop'), ('R&B', 'R&B'), ('Bongo', 'Bongo'), ('Chakacha', 'Chakacha'), ('Mugithi', 'Mugithi'), ('Traditional songs', 'Traditional songs')], max_length=50)),
                ('professional_type', models.CharField(choices=[('Music Educator', 'Music Educator'), ('BackUp Vocalist', 'BackUp Vocalist'), ('Singer/Songwriter', 'Singer/Songwriter'), ('Songwriter', 'Songwriter'), ('Dj', 'Dj'), ('Choir', 'Choir'), ('Band', 'Band'), ('Instrumentalist', 'Instrumentalist'), ('Sound Engineer', 'Sound Engineer'), ('Music Visualiser', 'Music Visualiser')], max_length=50)),
            ],
        ),
    ]

# Generated by Django 5.0.1 on 2024-03-13 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_remove_musician_available_remove_musician_bio_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successfulhire',
            name='completion_status',
            field=models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Done', 'Done')], default='Ongoing', max_length=20),
        ),
    ]

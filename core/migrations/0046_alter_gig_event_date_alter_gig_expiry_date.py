# Generated by Django 5.0.1 on 2024-03-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_alter_application_gig_alter_application_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='event_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='gig',
            name='expiry_date',
            field=models.DateTimeField(null=True),
        ),
    ]

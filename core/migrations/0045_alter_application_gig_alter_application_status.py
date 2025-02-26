# Generated by Django 5.0.1 on 2024-03-09 11:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_alter_application_gig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='gig',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.gig'),
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Submitted', max_length=20),
        ),
    ]

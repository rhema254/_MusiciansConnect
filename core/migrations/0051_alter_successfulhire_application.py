# Generated by Django 5.0.1 on 2024-03-13 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_alter_successfulhire_completion_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='successfulhire',
            name='application',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='successfulhire', to='core.application'),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-26 22:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_application_gig_alter_application_client_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='client',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='core.client'),
            preserve_default=False,
        ),
    ]

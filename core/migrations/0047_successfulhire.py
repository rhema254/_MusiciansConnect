# Generated by Django 5.0.1 on 2024-03-10 22:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_alter_gig_event_date_alter_gig_expiry_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SuccessfulHire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_status', models.CharField(choices=[('Ongoing', 'Ongoing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Ongoing', max_length=20)),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='successfulhire', to='core.application')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.client')),
                ('gig', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.gig')),
                ('musician', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.musician')),
            ],
        ),
    ]

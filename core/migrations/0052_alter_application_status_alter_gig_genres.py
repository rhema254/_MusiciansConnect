# Generated by Django 5.0.1 on 2024-03-14 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_alter_successfulhire_application'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.CharField(choices=[('Submitted', 'Submitted'), ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected'), ('Done', 'Done')], default='Submitted', max_length=20),
        ),
        migrations.AlterField(
            model_name='gig',
            name='genres',
            field=models.ManyToManyField(default='Jazz', related_name='gigs', to='core.genre'),
        ),
    ]

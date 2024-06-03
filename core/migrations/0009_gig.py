# Generated by Django 5.0.1 on 2024-02-14 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_gig_alter_musician_charge_rate_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(auto_created=True, auto_now_add=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('genre', models.CharField(choices=[('Soul', 'Soul'), ('Jazz', 'Jazz'), ('Benga', 'Benga'), ('Pop', 'Pop'), ('R&B', 'R&B'), ('Bongo', 'Bongo'), ('Chakacha', 'Chakacha'), ('Mugithi', 'Mugithi'), ('Traditional songs', 'Traditional songs')], max_length=20)),
                ('location', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Pending', 'Pending')], default='Open', max_length=20)),
                ('budget', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('l_budget', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('h_budget', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]

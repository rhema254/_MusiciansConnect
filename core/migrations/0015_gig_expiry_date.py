# Generated by Django 5.0.1 on 2024-02-16 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_gig_profession_category_alter_gig_dry_run_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='expiry_date',
            field=models.DateField(null=True),
        ),
    ]

# Generated by Django 4.2 on 2023-04-24 00:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imgapp', '0014_imagemetadata_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='day',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='imgapp.daypage'),
        ),
        migrations.AlterField(
            model_name='imagemetadata',
            name='capture_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

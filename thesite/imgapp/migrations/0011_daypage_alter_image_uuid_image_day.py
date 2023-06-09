# Generated by Django 4.2 on 2023-04-23 23:17

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('imgapp', '0010_alter_image_uuid_alter_imagemetadata_camera_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DayPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('caption', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='image',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=36),
        ),
        migrations.AddField(
            model_name='image',
            name='day',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='imgapp.daypage'),
        ),
    ]

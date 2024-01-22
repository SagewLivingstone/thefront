# Generated by Django 4.2 on 2024-01-22 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imgapp', '0021_alter_albumimage_caption'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['-day__date']},
        ),
        migrations.AddField(
            model_name='album',
            name='images',
            field=models.ManyToManyField(through='imgapp.AlbumImage', to='imgapp.image'),
        ),
        migrations.AddField(
            model_name='albumimage',
            name='bottom_caption',
            field=models.TextField(blank=True, null=True),
        ),
    ]

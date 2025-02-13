# Generated by Django 5.0.6 on 2024-06-29 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_playlist_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='playlisttrack',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='playlisttrack',
            name='order',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='playlisttrack',
            unique_together={('playlist', 'track')},
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-03 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0008_alter_players_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='players',
            name='old_teams',
            field=models.JSONField(default=dict, null=True, verbose_name='old teams'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='color',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

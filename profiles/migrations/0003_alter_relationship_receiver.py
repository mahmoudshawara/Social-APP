# Generated by Django 4.2.4 on 2023-09-17 22:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_alter_profile_avatar_relationship'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relationship',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='profiles.profile'),
        ),
    ]